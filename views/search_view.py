# search_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox  # Needed for error/warning dialogs

def create_search_view(parent_frame, parent_view):
    """Create the search view content"""
    # Main container
    main_frame = ttk.Frame(parent_frame)
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Title
    title_label = ttk.Label(main_frame, 
                           text="Search For Real Time Weather Data", 
                           font=("Arial", 14, "bold"))
    title_label.pack(pady=(0, 20))

    # Content wrapper to ensure consistent width between sections
    content_wrapper = ttk.Frame(main_frame)
    content_wrapper.pack()

    # Input section
    input_frame = ttk.LabelFrame(content_wrapper, text="Location Parameters", padding=15)
    input_frame.pack(pady=(0, 20), fill=X)

    input_frame.columnconfigure(0, weight=1)
    input_frame.columnconfigure(1, weight=0)  
    input_frame.columnconfigure(2, weight=0)  
    input_frame.columnconfigure(3, weight=0)  
    input_frame.columnconfigure(4, weight=1)  

    ttk.Label(input_frame, text="Enter Your City Name: ").grid(row=1, column=1, sticky=W, padx=(0, 10), pady=(10, 0))
    city_entry = ttk.Entry(input_frame, width=15)
    city_entry.grid(row=1, column=2, pady=(10, 0))

    def on_search_clicked():
        """Handle search button click"""
        city_name = city_entry.get().strip()
        if not city_name:
            messagebox.showerror("Invalid Input", "Please enter a city name.")
            return
        
        # Get the controller from the parent view and call the search handler
        if hasattr(parent_view, 'controller'):
            parent_view.controller.handle_search_request(city_name)
        else:
            # Fallback: call the refresh callback with the city name if controller not available
            # This would require modifying the callback to accept parameters
            messagebox.showwarning("Feature Unavailable", "Search functionality is not properly connected.")

    def on_enter_pressed(event):
        """Handle Enter key press in the city entry field"""
        on_search_clicked()

    search_btn = ttk.Button(input_frame, text="Find Current Weather", 
                           bootstyle="success", command=on_search_clicked)
    search_btn.grid(row=1, column=3, padx=(20, 0), pady=(10, 0))
    
    # Bind Enter key to the entry field
    city_entry.bind('<Return>', on_enter_pressed)

    # Results Frame (same container as input_frame)
    results_frame = ttk.LabelFrame(content_wrapper, text="🌤️ Weather Conditions", padding=15)
    results_frame.pack(pady=(0, 20), fill=X)

    results_frame.columnconfigure(0, weight=1)

    # Using grid for consistent layout
    temperature_label = ttk.Label(results_frame, text="Temperature: --", font=("Arial", 12))
    temperature_label.grid(row=0, column=0, sticky=W, pady=2)

    description_label = ttk.Label(results_frame, text="Conditions: --", font=("Arial", 12))
    description_label.grid(row=1, column=0, sticky=W, pady=2)

    humidity_label = ttk.Label(results_frame, text="Humidity: --", font=("Arial", 12))
    humidity_label.grid(row=2, column=0, sticky=W, pady=2)

    data_source_label = ttk.Label(main_frame, text="Data Source: Not loaded", font=("Arial", 9, "italic"))
    data_source_label.pack(pady=5)

    parent_view.search_temperature_label = temperature_label
    parent_view.search_description_label = description_label
    parent_view.search_humidity_label = humidity_label
    parent_view.search_data_source_label = data_source_label 