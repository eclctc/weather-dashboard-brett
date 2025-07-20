import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from typing import Callable, Dict, Optional
from models.pollen_model import PollenModel


class WeatherView:
    """View class responsible for the user interface."""

    def __init__(self, on_refresh_callback: Callable[[], None]):
        self.on_refresh_callback = on_refresh_callback
        self.current_theme = "flatly"
        self.available_themes = ["flatly", "darkly"]
        self.setup_main_window()
        self.setup_gui()

    def setup_main_window(self):
        self.main_window = ttk.Window(themename=self.current_theme)
        self.main_window.geometry("1200x500")
        self.main_window.title("Atlanta Weather & Pollen Tracker")
        self.main_window.resizable(False, False)

    def setup_gui(self):
        # --- Header ---
        header_frame = ttk.Frame(self.main_window, padding=10)
        header_frame.pack(fill=X)

        # Title + Date stacked vertically
        title_date_frame = ttk.Frame(header_frame)
        title_date_frame.pack(side=LEFT, anchor="w")

        title_label = ttk.Label(title_date_frame,
                                text="Atlanta, GA - Weather & Pollen Conditions",
                                font=("Arial", 16, "bold"))
        title_label.pack(anchor="w")

        self.date_label = ttk.Label(title_date_frame,
                                    text="Date: --",
                                    font=("Arial", 12, "italic", "bold"))
        self.date_label.pack(anchor="w", pady=(3, 0))

        # Theme toggle + refresh on the right
        theme_frame = ttk.Frame(header_frame)
        theme_frame.pack(side=RIGHT)

        ttk.Label(theme_frame, text="Dark Mode:").pack(side=LEFT, padx=5)
        self.dark_mode_var = ttk.BooleanVar(value=False)

        self.theme_switch = ttk.Checkbutton(
            theme_frame,
            variable=self.dark_mode_var,
            bootstyle="switch",
            command=self.toggle_theme
        )
        self.theme_switch.pack(side=LEFT, padx=5)

        self.refresh_button = ttk.Button(
            header_frame,
            text="🔄 Refresh Data",
            command=self._on_refresh_clicked,
            bootstyle="primary"
        )
        self.refresh_button.pack(side=RIGHT, padx=(0, 20))

        # --- Main Content ---
        main_frame = ttk.Frame(self.main_window, padding=10)
        main_frame.pack(fill=BOTH, expand=True)

        # --- Weather Column ---
        weather_frame = ttk.LabelFrame(main_frame, text="🌤️ Weather Conditions", padding=15)
        weather_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))

        self.temperature_label = ttk.Label(weather_frame, text="Temperature: --",
                                           font=("Arial", 12, "bold"))
        self.temperature_label.pack(anchor="w", pady=5)

        self.humidity_label = ttk.Label(weather_frame, text="Humidity: --",
                                        font=("Arial", 12))
        self.humidity_label.pack(anchor="w", pady=5)

        self.description_label = ttk.Label(weather_frame, text="Conditions: --",
                                           font=("Arial", 11))
        self.description_label.pack(anchor="w", pady=5)

        # --- Pollen Column ---
        pollen_frame = ttk.LabelFrame(main_frame, text="🌿 Pollen Levels", padding=15)
        pollen_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

        guide_frame = ttk.Frame(pollen_frame)
        guide_frame.pack(fill=X, pady=(0, 15))

        ttk.Label(guide_frame, text="Level Guide:", font=("Arial", 10, "bold")).pack(anchor="w")

        legend_row = ttk.Frame(guide_frame)
        legend_row.pack(fill=X, pady=(3, 0))

        legend_items = [
            ("●", "gray", "None"),
            ("●", "darkgreen", "Very Low"),
            ("●", "lightgreen", "Low"),
            ("●", "yellow", "Moderate"),
            ("●", "orange", "High"),
            ("●", "red", "Very High")
        ]
        for i, (symbol, color, text) in enumerate(legend_items):
            if i > 0:
                ttk.Label(legend_row, text=" • ", font=("Arial", 12)).pack(side=LEFT)
            ttk.Label(legend_row, text=symbol, font=("Arial", 12), foreground=color).pack(side=LEFT)
            ttk.Label(legend_row, text=text, font=("Arial", 12)).pack(side=LEFT, padx=(2, 0))

        # Grass
        grass_frame = ttk.Frame(pollen_frame)
        grass_frame.pack(fill=X, pady=5)

        ttk.Label(grass_frame, text="🌱", font=("Arial", 14)).pack(side=LEFT, padx=(0, 5))
        self.grass_label = ttk.Label(grass_frame, text="Grass: --", font=("Arial", 11))
        self.grass_label.pack(side=LEFT)
        self.grass_color_label = ttk.Label(grass_frame, text="●", font=("Arial", 20))
        self.grass_color_label.pack(side=RIGHT)

        # Tree
        tree_frame = ttk.Frame(pollen_frame)
        tree_frame.pack(fill=X, pady=5)

        ttk.Label(tree_frame, text="🌳", font=("Arial", 14)).pack(side=LEFT, padx=(0, 5))
        self.tree_label = ttk.Label(tree_frame, text="Tree: --", font=("Arial", 11))
        self.tree_label.pack(side=LEFT)
        self.tree_color_label = ttk.Label(tree_frame, text="●", font=("Arial", 20))
        self.tree_color_label.pack(side=RIGHT)

        # Weed
        weed_frame = ttk.Frame(pollen_frame)
        weed_frame.pack(fill=X, pady=5)

        ttk.Label(weed_frame, text="🌾", font=("Arial", 14)).pack(side=LEFT, padx=(0, 5))
        self.weed_label = ttk.Label(weed_frame, text="Weed: --", font=("Arial", 11))
        self.weed_label.pack(side=LEFT)
        self.weed_color_label = ttk.Label(weed_frame, text="●", font=("Arial", 20))
        self.weed_color_label.pack(side=RIGHT)

        # --- Health Column ---
        health_frame = ttk.LabelFrame(main_frame, text="🏥 Health Recommendations", padding=15)
        health_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(5, 0))

        self.health_text = ttk.Text(health_frame, height=15, width=35, wrap="word",
                                    font=("Arial", 12))
        scrollbar = ttk.Scrollbar(health_frame, orient="vertical", command=self.health_text.yview)
        self.health_text.configure(yscrollcommand=scrollbar.set)

        self.health_text.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # --- Status Bar ---
        status_frame = ttk.Frame(self.main_window, padding=5)
        status_frame.pack(fill=X, side=BOTTOM)

        self.weather_source_label = ttk.Label(status_frame, text="Weather: Not loaded",
                                              font=("Arial", 8, "italic"))
        self.weather_source_label.pack(side=LEFT)

        self.pollen_source_label = ttk.Label(status_frame, text="Pollen: Not loaded",
                                             font=("Arial", 8, "italic"))
        self.pollen_source_label.pack(side=RIGHT)

    def change_theme(self, new_theme):
        self.main_window.style.theme_use(new_theme)
        self.current_theme = new_theme

    def toggle_theme(self):
        new_theme = "darkly" if self.dark_mode_var.get() else "flatly"
        self.change_theme(new_theme)

    def _on_refresh_clicked(self):
        self.on_refresh_callback()

    def update_display(self, weather_data: Optional[Dict], weather_source: str,
                       pollen_data: Optional[Dict], pollen_source: str):
        if weather_data:
            self.temperature_label.config(text=f"Temperature: {weather_data['temp']}°F")
            self.humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
            self.description_label.config(text=f"Conditions: {weather_data['description'].title()}")
            self.date_label.config(text=f"Date: {weather_data['date']}")
        else:
            self.clear_weather_labels()

        if pollen_data:
            self.update_pollen_display(pollen_data)
        else:
            self.clear_pollen_labels()

        self.weather_source_label.config(text=f"Weather: {weather_source}")
        self.pollen_source_label.config(text=f"Pollen: {pollen_source}")

    def update_pollen_display(self, pollen_data: Dict):
        self.grass_label.config(text=f"Grass: {PollenModel.get_pollen_level_text(pollen_data['grass'])}")
        self.grass_color_label.config(foreground=PollenModel.get_pollen_color(pollen_data['grass']))

        self.tree_label.config(text=f"Tree: {PollenModel.get_pollen_level_text(pollen_data['tree'])}")
        self.tree_color_label.config(foreground=PollenModel.get_pollen_color(pollen_data['tree']))

        self.weed_label.config(text=f"Weed: {PollenModel.get_pollen_level_text(pollen_data['weed'])}")
        self.weed_color_label.config(foreground=PollenModel.get_pollen_color(pollen_data['weed']))

        self.health_text.config(state="normal")
        self.health_text.delete(1.0, "end")
        recs = pollen_data.get("health_recommendations", [])
        if recs:
            for i, rec in enumerate(recs):
                if i > 0:
                    self.health_text.insert("end", "\n\n")
                self.health_text.insert("end", f"• {rec}")
        else:
            self.health_text.insert("end", "No specific health recommendations available at this time.")
        self.health_text.config(state="disabled")

    def clear_weather_labels(self):
        self.temperature_label.config(text="Temperature: --")
        self.humidity_label.config(text="Humidity: --")
        self.description_label.config(text="Conditions: --")
        self.date_label.config(text="Date: --")

    def clear_pollen_labels(self):
        self.grass_label.config(text="Grass: --")
        self.grass_color_label.config(foreground="gray")
        self.tree_label.config(text="Tree: --")
        self.tree_color_label.config(foreground="gray")
        self.weed_label.config(text="Weed: --")
        self.weed_color_label.config(foreground="gray")
        self.health_text.config(state="normal")
        self.health_text.delete(1.0, "end")
        self.health_text.insert("end", "No health recommendations loaded.")
        self.health_text.config(state="disabled")

    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)

    def show_warning(self, title: str, message: str):
        messagebox.showwarning(title, message)

    def run(self):
        self.main_window.mainloop()
