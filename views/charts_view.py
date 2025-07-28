import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from features import graph_logic

def create_charts_view(parent_frame, parent_view):
    """Create the charts view content"""
    # Main container
    main_frame = ttk.Frame(parent_frame)
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Title
    title_label = ttk.Label(main_frame, 
                           text="Historical Weather & Pollen Charts", 
                           font=("Arial", 14, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Chart type selection
    chart_frame = ttk.LabelFrame(main_frame, text="Chart Options", padding=10)
    chart_frame.pack(fill=X, pady=(0, 20))
    
    chart_var = ttk.StringVar(value="pollen")
    
    temp_radio = ttk.Radiobutton(chart_frame, text="Temperature Trends", 
                                variable=chart_var, value="temperature")
    temp_radio.pack(anchor=W)
    
    pollen_radio = ttk.Radiobutton(chart_frame, text="Pollen Count Trends", 
                                  variable=chart_var, value="pollen")
    pollen_radio.pack(anchor=W)
    
    combined_radio = ttk.Radiobutton(chart_frame, text="Combined Analysis", 
                                    variable=chart_var, value="combined")
    combined_radio.pack(anchor=W)
    
    # Chart display frame (create this before the button so we can reference it)
    chart_display = ttk.Frame(main_frame, relief="sunken", borderwidth=2)
    chart_display.pack(fill=BOTH, expand=True, pady=(20, 0))
    
    # Initial placeholder
    placeholder_label = ttk.Label(chart_display, 
                                 text="Select a chart type and click 'Generate Chart' to display visualization", 
                                 font=("Arial", 12))
    placeholder_label.pack(expand=True)
    
    def generate_chart():
        """Generate the selected chart type"""
        selected_chart = chart_var.get()
        try:
            # Clear the placeholder
            for widget in chart_display.winfo_children():
                widget.destroy()
            
            # Generate the chart
            graph_logic.chart_data(chart_display, selected_chart)
            
        except Exception as e:
            # Show error message if chart generation fails
            error_label = ttk.Label(chart_display, 
                                   text=f"Error generating chart: {str(e)}", 
                                   font=("Arial", 12),
                                   foreground="red")
            error_label.pack(expand=True)
    
    # Generate chart button
    generate_btn = ttk.Button(chart_frame, text="Generate Chart", 
                             bootstyle="primary",
                             command=generate_chart)
    generate_btn.pack(pady=10)