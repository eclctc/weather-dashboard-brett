import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta #To handle timestamps.
import time # For delays, rate limiting, and timestamps.
import json # For handling JSON responses (used implicitly).
import logging # For tracking activity, errors, and debugging info.
from typing import Dict, List, Optional, Tuple # Provides type hints like Tupel. Dict, List and Optional.

# Load environment variables from .env file
load_dotenv()

class WeatherModel:
    """Model class responsible for weather data operations and API interactions."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.api_key = api_key or os.getenv('OPENWEATHER_API_KEY')

        if not self.api_key:
            raise ValueError("API key not found. Please set OPENWEATHER_API_KEY in .env file or pass api_key parameter.")
        self.session = requests.Session()  # Reuse connections & keeps connections alive
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum seconds between requests
                
    def _respect_rate_limit(self):
        """Ensure we don't exceed API rate limits.
        Checks how long it's been since the last API request.
        If not enough time has passed (based on the rate limit), it pauses the program.
        Ensures we don't accidentally get blocked for making too many requests too quickly.
        """
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        self.last_request_time = time.time()
    
    def fetch_weather_data(self, city_name: str) -> Tuple[Optional[Dict], str]:
        """
        Fetches weather data for a given city from the OpenWeatherMap API.
        
        Args:
            city_name: Name of the city to get weather for
            
        Returns:
            Tuple of (weather_data_dict, source_info_string)
            weather_data_dict is None if fetch failed
        """
        self._respect_rate_limit()

        weather_data = None
        source_info = "Open Weather API Data"

        # Attempts up to 3 retries if errors occur.
        max_retries = 3
        retry_delays = [1, 2, 4]  # Exponential backoff        
        for attempt in range(max_retries):
            try:
                # Build the URL for the API request
                city_name = city_name.lower().strip() # Make sure that we're passing lower case and stripping the whitespace into the API
                full_api_url = f"{self.api_base_url}?q={city_name}&appid={self.api_key}&units=imperial"

                # Send the request and get the response
                response = requests.get(full_api_url, timeout=10)
                response.raise_for_status()
                
                # Convert the response into a dictionary
                json_data = response.json()
                
                # Check if the API returned an error (e.g., city not found)
                if json_data.get("cod") == "404":
                    raise ValueError("City not found by API.")
                
                # Extract the weather details we need from the dictionary
                
                # Convert datetime from UNIX timestamp for CSV file
                timestamp = json_data["dt"] 
                timestamp = datetime.utcfromtimestamp(timestamp).date()
                
                weather_data = {
                    "date": timestamp,
                    "temp": json_data['main']['temp'],
                    "description": json_data['weather'][0]['description'],
                    "humidity": json_data['main']['humidity']
                }

                return weather_data, source_info
                
            except requests.exceptions.RequestException as e:
                source_info = f"API Failed (Network): {e}"
            except ValueError as e:
                if "429" in str(e):
                    source_info = "API Failed (Rate Limited): Waiting 60 seconds..."
                    time.sleep(60)  # Wait 1 minute
                    continue  # Retry the loop
                else:
                    source_info = f"API Failed (Data): {e}"
            except KeyError as e:
                source_info = f"API Failed (Parse): Missing key {e}"
            except Exception as e:
                source_info = f"API Failed (Unknown): {e}"
                        # Wait before retry (except on last attempt)
            
            if attempt < max_retries - 1:
                time.sleep(retry_delays[attempt])
                # If all attempts fail, update the UI with the critical error and return None.
                source_info = f"Failed to fetch data after {max_retries} attempts"
                return None
    
    def validate_city_name(self, city_name: str) -> bool:
        """
        Validates if the city name is valid (not empty after stripping whitespace).
        
        Args:
            city_name: City name to validate
            
        Returns:
            True if valid, False otherwise
        """
        return bool(city_name.strip())
