import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone # To handle timestamps.
import time # For delays, rate limiting, and timestamps.
import json # For handling JSON responses (used implicitly).
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
        self._respect_rate_limit() # Ensure rate limits are not exceeded

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
                response.raise_for_status() # Check if an HTTP request was successful
                
                # Convert the response into a dictionary
                json_data = response.json()
                
                # Extract the weather details we need from the dictionary    
                timestamp = json_data["dt"]

                # Convert datetime from UNIX timestamp for CSV file
                timestamp = datetime.fromtimestamp(timestamp, tz=timezone.utc).date()
                
                weather_data = {
                    "date": timestamp,
                    "temp": json_data['main']['temp'],
                    "description": json_data['weather'][0]['description'],
                    "humidity": json_data['main']['humidity']
                }

                return weather_data, source_info
                
            except requests.exceptions.Timeout:
                source_info = f"API request timed out (attempt {attempt + 1}/{max_retries})"
                if attempt < max_retries - 1:
                    time.sleep(retry_delays[attempt])
                    continue
                    
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Rate limited
                    source_info = f"API rate limited (attempt {attempt + 1}/{max_retries}): Waiting 60 seconds..."
                    time.sleep(60)  # Wait 1 minute
                    continue
                else:
                    source_info = f"{e.response.status_code}"
                    if attempt < max_retries - 1:
                        time.sleep(retry_delays[attempt])
                        continue
                        
            except requests.exceptions.RequestException as e:
                source_info = f"API network error (attempt {attempt + 1}/{max_retries}): {e}"
                if attempt < max_retries - 1:
                    time.sleep(retry_delays[attempt])
                    continue
                    
            except Exception as e:
                source_info = f"Unexpected error (attempt {attempt + 1}/{max_retries}): {e}"
                if attempt < max_retries - 1:
                    time.sleep(retry_delays[attempt])
                    continue
        
        # If all attempts fail, return final error message
        source_info = f"Failed to fetch weather data after {max_retries} attempts. Last error: {source_info}"
        return None, source_info