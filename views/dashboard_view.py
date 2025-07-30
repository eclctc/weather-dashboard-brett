import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from typing import Callable, Dict, Optional
from models.pollen_model import PollenModel
import pandas as pd
from datetime import datetime, timedelta

# Matplotlib imports for tkinter integration
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.dates as mdates

## Import views for tabs
from views import charts_view
from views import prediction_view
from views import search_view
from views import team_view


class WeatherView:
    """View class responsible for the user interface."""

    def __init__(self, on_refresh_callback: Callable[[], None]):
        self.on_refresh_callback = on_refresh_callback
        self.current_theme = "darkly"
        self.available_themes = ["flatly", "darkly"]
        self.pollen_data_df = None  # Store the pollen dataset
        self.setup_main_window()
        self.setup_gui()
        self.load_pollen_dataset()

    def setup_main_window(self):
        self.main_window = ttk.Window(themename=self.current_theme)
        self.main_window.geometry("1200x800")
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

        ttk.Label(theme_frame, text="Light Mode:").pack(side=LEFT, padx=5)
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
        
        # --- Tabs ---
        notebook = ttk.Notebook(self.main_window, bootstyle="primary")
        notebook.pack(fill=BOTH, expand=True)

        # Dashboard tab
        self.main_tab = ttk.Frame(notebook)
        notebook.add(self.main_tab, text="Dashboard")
        # ADD DASHBOARD CONTENT
        self.setup_dashboard_content()

        # Search tab - using imported search_view
        self.search_tab = ttk.Frame(notebook)
        notebook.add(self.search_tab, text="Search")
        search_view.create_search_view(self.search_tab, self)


        # # Prediction tab - using imported prediction_view
        self.prediction_tab = ttk.Frame(notebook)
        notebook.add(self.prediction_tab, text="Prediction")
        prediction_view.create_prediction_view(self.prediction_tab, self)

        # Team tab - using imported team_view
        self.team_tab = ttk.Frame(notebook)
        notebook.add(self.team_tab, text="weatherYouLikeItOrNot")
        team_view.create_team_view(self.team_tab, self)

    def setup_dashboard_content(self):
        """Setup the main dashboard content inside the Dashboard tab"""
        
        # --- Main Content --- (Parent is now self.main_tab)
        main_frame = ttk.Frame(self.main_tab, padding=10)
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

        # --- Chart Section --- (Parent is now self.main_tab)
        chart_frame = ttk.LabelFrame(self.main_tab, text="📊 Pollen Trends (Last Year - Same Week)", padding=10)
        chart_frame.pack(fill=BOTH, expand=False, padx=10, pady=(0, 10))

        # Create matplotlib figure and canvas
        self.fig = Figure(figsize=(12, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Initialize with empty plot
        self.ax.set_title("Pollen Levels - Same Week Last Year")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Pollen Count")
        self.ax.grid(True, alpha=0.3)
        
        # Create canvas and add to tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

        # --- Status Bar --- (Parent is now self.main_tab)
        status_frame = ttk.Frame(self.main_tab, padding=5)
        status_frame.pack(fill=X, side=BOTTOM)

        self.weather_source_label = ttk.Label(status_frame, text="Weather: Not loaded",
                                              font=("Arial", 8, "italic"))
        self.weather_source_label.pack(side=LEFT)

        self.pollen_source_label = ttk.Label(status_frame, text="Pollen: Not loaded",
                                             font=("Arial", 8, "italic"))
        self.pollen_source_label.pack(side=RIGHT)

    def load_pollen_dataset(self):
        """Load the pollen dataset from CSV file"""
        try:
            self.pollen_data_df = pd.read_csv('data/pollen_atlanta_23_24.csv')
            # Ensure date column is datetime
            self.pollen_data_df['date'] = pd.to_datetime(self.pollen_data_df['date'])
            self.update_historical_chart()
        except FileNotFoundError:
            print("Warning: Pollen dataset not found at data/pollen_atlanta_23_24.csv")
        except Exception as e:
            print(f"Error loading pollen dataset: {e}")

    def set_pollen_dataset(self, df: pd.DataFrame):
        """Set the pollen dataset for historical chart display"""
        self.pollen_data_df = df.copy()
        # Ensure date column is datetime
        self.pollen_data_df['date'] = pd.to_datetime(self.pollen_data_df['date'])
        self.update_historical_chart()

    def update_historical_chart(self):
        """Update the chart with historical pollen data from the same week last year"""
        if self.pollen_data_df is None or self.pollen_data_df.empty:
            return

        # Clear the current plot
        self.ax.clear()

        # Get current date and calculate last year's date range
        current_date = datetime.now().date()
        last_year_end_date = current_date.replace(year=current_date.year - 1)
        last_year_start_date = last_year_end_date - timedelta(days=6)  # 7 days total

        # Filter data for the 7-day period from last year
        filtered_data = self.pollen_data_df[
            (self.pollen_data_df['date'].dt.date >= last_year_start_date) &
            (self.pollen_data_df['date'].dt.date <= last_year_end_date)
        ].copy()

        if filtered_data.empty:
            self.ax.text(0.5, 0.5, 'No historical data available for this week last year', 
                        horizontalalignment='center', verticalalignment='center', 
                        transform=self.ax.transAxes, fontsize=12)
            self.ax.set_title(f"Pollen Levels - {last_year_start_date.strftime('%b %d')} to {last_year_end_date.strftime('%b %d, %Y')}")
        else:
            # Sort by date
            filtered_data = filtered_data.sort_values('date')
            
            # Plot the three pollen types
            self.ax.plot(filtered_data['date'], filtered_data['Count.tree_pollen'], 
                        marker='o', linewidth=2, label='Tree Pollen', color='#2E8B57')
            self.ax.plot(filtered_data['date'], filtered_data['Count.grass_pollen'], 
                        marker='s', linewidth=2, label='Grass Pollen', color='#32CD32')
            self.ax.plot(filtered_data['date'], filtered_data['Count.weed_pollen'], 
                        marker='^', linewidth=2, label='Weed Pollen', color='#DAA520')

            # Format x-axis dates
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
            self.ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
            
            # Rotate x-axis labels for better readability
            plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)
            
            # Set title with date range
            self.ax.set_title(f"Pollen Levels - {last_year_start_date.strftime('%b %d')} to {last_year_end_date.strftime('%b %d, %Y')}")
            
            # Add legend
            self.ax.legend(loc='upper right')

        # Set labels and grid
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Pollen Count")
        self.ax.grid(True, alpha=0.3)
        
        # Apply current theme to chart
        self.update_chart_theme()
        
        # Adjust layout and refresh canvas
        self.fig.tight_layout()
        self.canvas.draw()

    def update_chart_theme(self):
        """Update chart colors based on current theme"""
        if self.current_theme == "darkly":
            # Dark theme colors
            self.fig.patch.set_facecolor('#2b2b2b')
            self.ax.set_facecolor('#2b2b2b')
            self.ax.tick_params(colors='white')
            self.ax.xaxis.label.set_color('white')
            self.ax.yaxis.label.set_color('white')
            self.ax.title.set_color('white')
            self.ax.grid(True, alpha=0.3, color='white')
            # Update legend text color if legend exists
            legend = self.ax.get_legend()
            if legend:
                for text in legend.get_texts():
                    text.set_color('white')
                # Update background color and edge color
                legend.get_frame().set_facecolor('black') 
        else:
            # Light theme colors
            self.fig.patch.set_facecolor('white')
            self.ax.set_facecolor('white')
            self.ax.tick_params(colors='black')
            self.ax.xaxis.label.set_color('black')
            self.ax.yaxis.label.set_color('black')
            self.ax.title.set_color('black')
            self.ax.grid(True, alpha=0.3, color='black')
            # Update legend text color if legend exists
            legend = self.ax.get_legend()
            if legend:
                for text in legend.get_texts():
                    text.set_color('black')
                legend.get_frame().set_facecolor('white')
        self.canvas.draw()

    def change_theme(self, new_theme):
        self.main_window.style.theme_use(new_theme)
        self.current_theme = new_theme
        self.update_chart_theme()

    def toggle_theme(self):
        new_theme = "flatly" if self.dark_mode_var.get() else "darkly"
        self.change_theme(new_theme)

    def _on_refresh_clicked(self):
        self.on_refresh_callback()

    def update_display(self, weather_data: Optional[Dict], weather_source: str,
                    pollen_data: Optional[Dict], pollen_source: str):
        """Update Dashboard tab displays with weather data"""
        
        # Update Dashboard tab only
        if weather_data:
            self.temperature_label.config(text=f"Temperature: {weather_data['temp']}°F")
            self.humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
            self.description_label.config(text=f"Conditions: {weather_data['description'].title()}")
            self.date_label.config(text=f"Date: {weather_data['date']}")
        else:
            self.clear_weather_labels()

        # Update pollen data
        if pollen_data:
            self.update_pollen_display(pollen_data)
        else:
            self.clear_pollen_labels()

        # Update source labels
        self.weather_source_label.config(text=f"Weather: {weather_source}")
        self.pollen_source_label.config(text=f"Pollen: {pollen_source}")

    def update_search_display(self, weather_data: Optional[Dict], weather_source: str):
        """Update Search tab displays with weather data"""
        if hasattr(self, 'search_temperature_label'):
            if weather_data:
                self.search_temperature_label.config(text=f"Temperature: {weather_data['temp']}°F")
                self.search_description_label.config(text=f"Conditions: {weather_data['description'].title()}")
                self.search_humidity_label.config(text=f"Humidity: {weather_data['humidity']}%")
                self.search_data_source_label.config(text=f"Data Source: {weather_source}")
            else:
                self.search_temperature_label.config(text="Temperature: Unable to load")
                self.search_description_label.config(text="Conditions: Unable to load")
                self.search_humidity_label.config(text="Humidity: Unable to load")
                self.search_data_source_label.config(text=f"Data Source: {weather_source}")
        
        # Force GUI update
        self.main_window.update_idletasks()

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
    
    def set_controller(self, controller):
        """Set reference to the controller for search functionality"""
        self.controller = controller    

    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)

    def show_warning(self, title: str, message: str):
        messagebox.showwarning(title, message)

    def run(self):
        self.main_window.mainloop()