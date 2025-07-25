import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.weather_model import WeatherModel
from models.pollen_model import PollenModel
from features.weather_logger import WeatherLogger
from views.dashboard_view import WeatherView


class WeatherController:
    """Controller class that coordinates between the models (data layer) and view (Tkinter GUI)."""
    
    def __init__(self):
        # Initialize models and logger
        self.weather_model = WeatherModel()
        self.pollen_model = PollenModel()
        self.weather_logger = WeatherLogger()
        
        # Initialize view with callback
        self.weather_view = WeatherView(self.handle_data_refresh_request)
        
        # Set controller reference in view for search functionality
        self.weather_view.set_controller(self)

        # Load initial data for Atlanta
        self.load_atlanta_data()
        
        # Start the application
        self.weather_view.run()
    
    def load_atlanta_data(self):
        """Load weather and pollen data for Atlanta, GA on startup."""
        self.handle_data_refresh_request()
    
    def handle_data_refresh_request(self, city_name=None):
        """
        Handles the data refresh request from the view.
        Fetches both weather and pollen data for the specified city or Atlanta as default.
        
        Args:
            city_name (str, optional): Name of city to fetch data for. Defaults to "Atlanta".
        """
        # Use provided city name or default to Atlanta
        target_city = city_name if city_name else "Atlanta"
        
        # Fetch weather data for the target city
        weather_data, weather_source = self.weather_model.fetch_weather_data(target_city)
        
        # Fetch pollen data (keeping Atlanta as default since pollen model might be location-specific)
        # You may want to modify this if your pollen model supports other cities
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
            log_error = self.weather_logger.log_weather_data(target_city, weather_data, weather_source)
            if log_error:
                    self.weather_view.show_warning("File Write Error", log_error)
    
    def handle_search_request(self, city_name):
        """
        Handle search requests from the search view.
        This updates ONLY the search tab, not the dashboard.
        
        Args:
            city_name (str): Name of city to search for weather data
        """
        if not city_name or not city_name.strip():
            self.weather_view.show_error("Invalid Input", "Please enter a valid city name.")
            return
        
        # Fetch weather data for the searched city
        weather_data, weather_source = self.weather_model.fetch_weather_data(city_name.strip())
        
        # Handle weather API errors
        if weather_data is None:
            if "404" in weather_source:
                self.weather_view.show_error("Weather Network Error", f"Could not connect to weather service. {weather_source}")
            else:
                self.weather_view.show_error("Weather Error", f"Weather error occurred: {weather_source}")
        
        # Update ONLY the search display (not the main dashboard)
        self.weather_view.update_search_display(weather_data, weather_source)
        
        # Log the weather data (if available)
        if weather_data:
            log_error = self.weather_logger.log_weather_data(city_name.strip(), weather_data, weather_source)
            if log_error:
                self.weather_view.show_warning("File Write Error", log_error)
                

if __name__ == "__main__":
    WeatherController()