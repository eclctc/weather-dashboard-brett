import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone
import time
from typing import Dict, Optional, Tuple

# Load environment variables from .env file
load_dotenv()

class PollenModel:
    """Model class responsible for pollen data operations and Google Pollen API interactions."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_base_url = "https://pollen.googleapis.com/v1/forecast:lookup"
        self.api_key = api_key or os.getenv('GOOGLE_POLLEN_API_KEY')

        if not self.api_key:
            raise ValueError("Google Pollen API key not found. Please set GOOGLE_POLLEN_API_KEY in .env file or pass api_key parameter.")

        self.session = requests.Session()
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum seconds between requests

        # Atlanta coordinates
        self.atlanta_lat = 33.749
        self.atlanta_lon = -84.388

    def _respect_rate_limit(self):
        """Ensure we don't exceed API rate limits."""
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def fetch_pollen_data(self) -> Tuple[Optional[Dict], str]:
        """
        Fetches pollen data for Atlanta from the Google Pollen API.

        Returns:
            Tuple of (pollen_data_dict, source_info_string)
            pollen_data_dict is None if fetch failed
        """
        self._respect_rate_limit()

        pollen_data = None
        source_info = "Google Pollen API Data"

        # Retry logic
        max_retries = 3
        retry_delays = [1, 2, 4]

        for attempt in range(max_retries):
            try:
                params = {
                    'key': self.api_key,
                    'location.longitude': self.atlanta_lon,
                    'location.latitude': self.atlanta_lat,
                    'days': 1
                }

                response = requests.get(self.api_base_url, params=params, timeout=10)
                response.raise_for_status()

                json_data = response.json()

                # Extract pollen data from the response
                if 'dailyInfo' in json_data and len(json_data['dailyInfo']) > 0:
                    daily_info = json_data['dailyInfo'][0]

                    # Extract pollen counts and health recommendations
                    pollen_types = daily_info.get('pollenTypeInfo', [])

                    # Initialize with default values
                    grass_index = 0
                    tree_index = 0
                    weed_index = 0
                    health_recommendations = []

                    # Parse pollen data and recommendations
                    for pollen_type in pollen_types:
                        code = pollen_type.get('code', '')
                        index_info = pollen_type.get('indexInfo', {})
                        value = index_info.get('value', 0)

                        if code == 'GRASS':
                            grass_index = value
                        elif code == 'TREE':
                            tree_index = value
                        elif code == 'WEED':
                            weed_index = value

                        # Extract any health recommendations tied to this pollen type
                        recs = pollen_type.get('healthRecommendations', [])
                        for rec in recs:
                            recommendation_text = rec
                            if recommendation_text:
                                health_recommendations.append(f"{code.title()}: {recommendation_text}")                    
                                break
                    pollen_data = {
                        'grass': grass_index,
                        'tree': tree_index,
                        'weed': weed_index,
                        'health_recommendations': health_recommendations
                    }

                    return pollen_data, source_info
                else:
                    source_info = "No pollen data available in API response"
                    return None, source_info

            except requests.exceptions.Timeout:
                source_info = f"Pollen API request timed out (attempt {attempt + 1}/{max_retries})"
                if attempt < max_retries - 1:
                    time.sleep(retry_delays[attempt])
                    continue

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Rate limited
                    source_info = f"Pollen API rate limited (attempt {attempt + 1}/{max_retries}): Waiting 60 seconds..."
                    time.sleep(60)
                    continue
                else:
                    source_info = f"Pollen API HTTP Error: {e.response.status_code}"
                    if attempt < max_retries - 1:
                        time.sleep(retry_delays[attempt])
                        continue

            except requests.exceptions.RequestException as e:
                source_info = f"Pollen API network error (attempt {attempt + 1}/{max_retries}): {e}"
                if attempt < max_retries - 1:
                    time.sleep(retry_delays[attempt])
                    continue

            except Exception as e:
                source_info = f"Unexpected pollen API error (attempt {attempt + 1}/{max_retries}): {e}"
                if attempt < max_retries - 1:
                    time.sleep(retry_delays[attempt])
                    continue

        # If all attempts fail, return final error message
        source_info = f"Failed to fetch pollen data after {max_retries} attempts. Last error: {source_info}"
        return None, source_info

    @staticmethod
    def get_pollen_color(index: int) -> str:
        """
        Returns the color code for a given pollen index.

        Args:
            index: Pollen index (0-5)

        Returns:
            Color name for the pollen level
        """
        color_map = {
            0: "gray",
            1: "darkgreen",
            2: "lightgreen",
            3: "yellow",
            4: "orange",
            5: "red"
        }
        return color_map.get(index, "gray")

    @staticmethod
    def get_pollen_level_text(index: int) -> str:
        """
        Returns the text description for a given pollen index.

        Args:
            index: Pollen index (0-5)

        Returns:
            Text description of the pollen level
        """
        level_map = {
            0: "None",
            1: "Very Low",
            2: "Low",
            3: "Moderate",
            4: "High",
            5: "Very High"
        }
        return level_map.get(index, "Unknown")