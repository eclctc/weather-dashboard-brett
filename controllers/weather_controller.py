import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.weather_model import WeatherModel
from features.weather_logger import WeatherLogger
from views.weather_view import WeatherView

class WeatherController:
    """Controller class that coordinates between the model (data layer) and view (Tkinter GUI)."""
    
    def __init__(self):
        # Initialize model and logger
        self.weather_model = WeatherModel()
        self.weather_logger = WeatherLogger()
        
        # Initialize view with callback
        self.weather_view = WeatherView(self.handle_get_weather_request)
        
        # Start the application
        self.weather_view.run()
    
    def handle_get_weather_request(self, city_name: str):
        """
        Handles the weather request from the view.
        
        Args:
            city_name: Name of the city to get weather for
        """
        # Validate city name
        if not self.weather_model.validate_city_name(city_name):
            self.weather_view.show_warning("Input Error", "Please enter a city name.")
            self.weather_view.clear_weather_labels()
            return
        
        # Fetch weather data
        weather_data, source_info = self.weather_model.fetch_weather_data(city_name)
        
        # Handle API errors
        if weather_data is None:
            if "404" in source_info:
                self.weather_view.show_error("Network Error", f"Could not connect to weather service. {source_info}")
            else:
                self.weather_view.show_error("Unknown Error", f"An unexpected error occurred: {source_info}")
        
        # Update the view
        self.weather_view.update_weather_display(weather_data, source_info)
        
        # Log the data
        if weather_data:
            log_error = self.weather_logger.log_weather_data(city_name, weather_data, source_info)
            if log_error:
                self.weather_view.show_warning("File Write Error", log_error)

if __name__ == "__main__":
    WeatherController()