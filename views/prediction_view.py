import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def create_prediction_view(parent_frame, parent_view):
    """Create the prediction view content"""
    # Main container
    main_frame = ttk.Frame(parent_frame)
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Title
    title_label = ttk.Label(main_frame, 
                           text="Weather & Pollen Prediction Model", 
                           font=("Arial", 14, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Input section
    input_frame = ttk.LabelFrame(main_frame, text="Input Parameters", padding=15)
    input_frame.pack(fill=X, pady=(0, 20))
    
    # Create input fields in a grid
    ttk.Label(input_frame, text="Temperature (°F):").grid(row=0, column=0, sticky=W, padx=(0, 10))
    temp_entry = ttk.Entry(input_frame, width=15)
    temp_entry.grid(row=0, column=1, padx=(0, 20))
    
    ttk.Label(input_frame, text="Humidity (%):").grid(row=0, column=2, sticky=W, padx=(0, 10))
    humidity_entry = ttk.Entry(input_frame, width=15)
    humidity_entry.grid(row=0, column=3)
    
    ttk.Label(input_frame, text="Wind Speed (mph):").grid(row=1, column=0, sticky=W, padx=(0, 10), pady=(10, 0))
    wind_entry = ttk.Entry(input_frame, width=15)
    wind_entry.grid(row=1, column=1, padx=(0, 20), pady=(10, 0))
    
    ttk.Label(input_frame, text="Precipitation (in):").grid(row=1, column=2, sticky=W, padx=(0, 10), pady=(10, 0))
    precip_entry = ttk.Entry(input_frame, width=15)
    precip_entry.grid(row=1, column=3, pady=(10, 0))
    
    # Predict button
    predict_btn = ttk.Button(input_frame, text="Generate Prediction", 
                            bootstyle="success")
    predict_btn.grid(row=2, column=1, columnspan=2, pady=20)
    
    # Results section
    results_frame = ttk.LabelFrame(main_frame, text="Prediction Results", padding=15)
    results_frame.pack(fill=BOTH, expand=True)
    
    # Results display
    results_text = ttk.Text(results_frame, height=10, wrap=WORD)
    results_scrollbar = ttk.Scrollbar(results_frame, orient=VERTICAL, command=results_text.yview)
    results_text.configure(yscrollcommand=results_scrollbar.set)
    
    results_text.pack(side=LEFT, fill=BOTH, expand=True)
    results_scrollbar.pack(side=RIGHT, fill=Y)
    
    # Insert placeholder text
    results_text.insert("1.0", "Prediction results will appear here...\n\n" +
                               "Model will predict:\n" +
                               "• Temperature forecast\n" +
                               "• Pollen count levels\n" +
                               "• Risk categories for different pollen types")
    results_text.config(state="disabled")