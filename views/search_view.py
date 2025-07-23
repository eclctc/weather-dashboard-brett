# search_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def create_search_view(parent_frame, parent_view):
    """Create the search view content"""
    # Main container
    main_frame = ttk.Frame(parent_frame)
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Title
    title_label = ttk.Label(main_frame, 
                           text="Search Historical Data", 
                           font=("Arial", 14, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Search controls
    search_frame = ttk.LabelFrame(main_frame, text="Search Parameters", padding=15)
    search_frame.pack(fill=X, pady=(0, 20))
    
    # Date range
    date_frame = ttk.Frame(search_frame)
    date_frame.pack(fill=X, pady=(0, 10))
    
    ttk.Label(date_frame, text="Start Date:").pack(side=LEFT)
    start_date_entry = ttk.DateEntry(date_frame)
    start_date_entry.pack(side=LEFT, padx=(10, 20))
    
    ttk.Label(date_frame, text="End Date:").pack(side=LEFT)
    end_date_entry = ttk.DateEntry(date_frame)
    end_date_entry.pack(side=LEFT, padx=10)
    
    # Data type selection
    data_frame = ttk.Frame(search_frame)
    data_frame.pack(fill=X, pady=10)
    
    ttk.Label(data_frame, text="Data Type:").pack(side=LEFT)
    
    data_var = ttk.StringVar(value="both")
    weather_check = ttk.Checkbutton(data_frame, text="Weather Data", variable=data_var)
    weather_check.pack(side=LEFT, padx=10)
    
    pollen_check = ttk.Checkbutton(data_frame, text="Pollen Data", variable=data_var)
    pollen_check.pack(side=LEFT, padx=10)
    
    # Search button
    search_btn = ttk.Button(search_frame, text="Search", bootstyle="primary")
    search_btn.pack(pady=10)
    
    # Results section
    results_frame = ttk.LabelFrame(main_frame, text="Search Results", padding=10)
    results_frame.pack(fill=BOTH, expand=True)
    
    # Treeview for results
    columns = ("Date", "Temperature", "Humidity", "Pollen Count", "Risk Level")
    results_tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=15)
    
    # Configure columns
    for col in columns:
        results_tree.heading(col, text=col)
        results_tree.column(col, width=100)
    
    # Scrollbars
    v_scrollbar = ttk.Scrollbar(results_frame, orient=VERTICAL, command=results_tree.yview)
    h_scrollbar = ttk.Scrollbar(results_frame, orient=HORIZONTAL, command=results_tree.xview)
    results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
    
    # Pack treeview and scrollbars
    results_tree.pack(side=LEFT, fill=BOTH, expand=True)
    v_scrollbar.pack(side=RIGHT, fill=Y)
    h_scrollbar.pack(side=BOTTOM, fill=X)
    
    # Sample data
    sample_data = [
        ("2023-01-01", "45°F", "65%", "18", "Low"),
        ("2023-01-02", "42°F", "60%", "11", "Low"),
        ("2023-01-03", "48°F", "70%", "97", "Moderate"),
    ]
    
    for item in sample_data:
        results_tree.insert("", "end", values=item)