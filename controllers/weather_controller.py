import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.weather_model import WeatherModel
from models.pollen_model import PollenModel
from features.weather_logger import WeatherLogger
from views.weather_view import WeatherView

class WeatherController:
    """Controller class that coordinates between the models (data layer) and view (Tkinter GUI)."""
    
    def __init__(self):
        # Initialize models and logger
        self.weather_model = WeatherModel()
        self.pollen_model = PollenModel()
        self.weather_logger = WeatherLogger()
        
        # Initialize view with callback
        self.weather_view = WeatherView(self.handle_data_refresh_request)
        
        # Load initial data for Atlanta
        self.load_atlanta_data()
        
        # Start the application
        self.weather_view.run()
    
    def load_atlanta_data(self):
        """Load weather and pollen data for Atlanta, GA on startup."""
        self.handle_data_refresh_request()
    
    def handle_data_refresh_request(self):
        """
        Handles the data refresh request from the view.
        Fetches both weather and pollen data for Atlanta, GA.
        """
        # Fetch weather data for Atlanta
        weather_data, weather_source = self.weather_model.fetch_weather_data("Atlanta")
        
        # Fetch pollen data for Atlanta
        pollen_data, pollen_source = self.pollen_model.fetch_pollen_data()
        
        # Handle weather API errors
        if weather_data is None:
            if "404" in weather_source:
                self.weather_view.show_error("Weather Network Error", f"Could not connect to weather service. {weather_source}")
            else:
                self.weather_view.show_error("Weather Error", f"Weather error occurred: {weather_source}")
        
        # Handle pollen API errors
        if pollen_data is None:
            self.weather_view.show_warning("Pollen Data Warning", f"Could not fetch pollen data: {pollen_source}")
        
        # Update the view with both weather and pollen data
        self.weather_view.update_display(weather_data, weather_source, pollen_data, pollen_source)
        
        # Log the weather data (if available)
        if weather_data:
            log_error = self.weather_logger.log_weather_data("Atlanta", weather_data, weather_source)
            if log_error:
                self.weather_view.show_warning("File Write Error", log_error)

if __name__ == "__main__":
    WeatherController()