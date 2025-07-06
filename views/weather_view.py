import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from typing import Callable


class WeatherView:
    """View class responsible for the user interface."""

    def __init__(self, on_get_weather_callback: Callable[[str], None]):
        self.on_get_weather_callback = on_get_weather_callback
        self.current_theme = "flatly"
        self.available_themes = ["flatly", "darkly"]
        self.setup_main_window()
        self.setup_gui()

    def setup_main_window(self):
        """Sets up the main application window using ttkbootstrap."""
        self.main_window = ttk.Window(themename=self.current_theme)
        self.main_window.geometry("450x400")
        self.main_window.title("Simple Weather Viewer")

    def setup_gui(self):
        """Creates and arranges all the widgets for the weather application."""
        # Dark Mode check box
        theme_frame = ttk.Frame(self.main_window, padding=10)
        theme_frame.pack(fill=X)

        ttk.Label(theme_frame, text="Dark Mode:").pack(side=LEFT, padx=5)
        self.dark_mode_var = ttk.BooleanVar(value=False)  # Start in light mode (flatly)

        self.theme_switch = ttk.Checkbutton(
            theme_frame,
            variable=self.dark_mode_var,
            bootstyle="switch",
            command=self.toggle_theme
        )
        self.theme_switch.pack(side=LEFT, padx=5)

        # Input Frame
        input_frame = ttk.Frame(self.main_window, padding=10)
        input_frame.pack()

        ttk.Label(input_frame, text="Enter city name:").pack(side=LEFT, padx=5)

        self.city_entry = ttk.Entry(input_frame, width=25)
        self.city_entry.pack(side=LEFT, padx=5)

        self.get_weather_button = ttk.Button(
            self.main_window,
            text="Get Weather",
            command=self._on_get_weather_clicked
        )
        self.get_weather_button.pack(pady=10)

        # Results Frame
        results_frame = ttk.LabelFrame(self.main_window, text="Weather Info", padding=10)
        results_frame.pack(fill=X, padx=20)

        self.temperature_label = ttk.Label(results_frame, text="Temperature: --", font=("Arial", 12))
        self.temperature_label.pack(anchor="w", pady=2)

        self.description_label = ttk.Label(results_frame, text="Conditions: --", font=("Arial", 12))
        self.description_label.pack(anchor="w", pady=2)

        self.humidity_label = ttk.Label(results_frame, text="Humidity: --", font=("Arial", 12))
        self.humidity_label.pack(anchor="w", pady=2)

        self.data_source_label = ttk.Label(self.main_window, text="Data Source: Not loaded", font=("Arial", 9, "italic"))
        self.data_source_label.pack(pady=5)

    def change_theme(self, new_theme):
        """Changes the application's theme."""
        self.main_window.style.theme_use(new_theme)
        self.current_theme = new_theme
    
    def toggle_theme(self):
        """Toggles between light and dark themes using the switch."""
        new_theme = "darkly" if self.dark_mode_var.get() else "flatly"
        self.change_theme(new_theme)
    
    def _on_get_weather_clicked(self):
        """Internal method called when get weather button is clicked."""
        city_name = self.city_entry.get().strip()
        self.on_get_weather_callback(city_name)

    def update_weather_display(self, weather_data, source_info: str):
        """Updates the weather display with new data."""
        if weather_data:
            self.temperature_label.config(text=f"Temperature: {weather_data['temp']}°F")
            self.description_label.config(text=f"Conditions: {weather_data['description'].title()}")
            self.humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
        else:
            self.clear_weather_labels()

        self.data_source_label.config(text=f"Data Source: {source_info}")

    def clear_weather_labels(self):
        """Resets the weather display labels to their default state."""
        self.temperature_label.config(text="Temperature: --")
        self.description_label.config(text="Conditions: --")
        self.humidity_label.config(text="Humidity: --")

    def show_error(self, title: str, message: str):
        """Shows an error message dialog."""
        messagebox.showerror(title, message)

    def show_warning(self, title: str, message: str):
        """Shows a warning message dialog."""
        messagebox.showwarning(title, message)

    def run(self):
        """Starts the main event loop."""
        self.main_window.mainloop()
