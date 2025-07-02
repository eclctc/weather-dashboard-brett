from typing import Dict, Optional
import logging

class WeatherLogger:
    """Handles logging of weather data to files."""
    
    def __init__(self, log_file: str = "weather_log.csv"):
        self.log_file = log_file
    
    def log_weather_data(self, city_name: str, weather_data: Optional[Dict], source_info: str) -> Optional[str]:
        """
        Logs weather data to a file.
        
        Args:
            city_name: Name of the city
            weather_data: Dictionary containing weather information
            source_info: Information about data source
            
        Returns:
            Error message if logging failed, None if successful
        """
        if not weather_data:
            return "No weather data to log"
        
        try:
            with open(self.log_file, "a") as log_file:
                log_file.write(f"{weather_data['date']}, {city_name}, {weather_data['temp']}, {weather_data['description']}, {weather_data['humidity']}, {source_info}\n")
            return None
        except IOError as e:
            return f"Could not save data to log file: {e}"