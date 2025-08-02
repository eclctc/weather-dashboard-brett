# views/team_view.py

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from features import team_feature

# Set matplotlib to use non-interactive backend to prevent popups
plt.ioff()

def create_team_view(parent_frame, parent_view=None):
    """Embed Team Precipitation View into the provided notebook frame."""

    # Main container inside notebook tab
    main_frame = ttk.Frame(parent_frame)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Dropdown for fiscal months
    control_frame = ttk.Frame(main_frame)
    control_frame.pack(pady=10)

    ttk.Label(control_frame, text="Select Fiscal Month:").pack(side=tk.LEFT, padx=(0, 10))

    month_var = tk.StringVar()
    month_dropdown = ttk.Combobox(control_frame,
                                   textvariable=month_var,
                                   values=team_feature.FISCAL_MONTHS,
                                   state="readonly",
                                   width=20)
    month_dropdown.pack(side=tk.LEFT)

    # Chart container
    canvas_frame = ttk.Frame(main_frame)
    canvas_frame.pack(fill=tk.BOTH, expand=True)

    chart_canvas = None

    def update_chart(event=None):
        nonlocal chart_canvas
        month = month_var.get()
        if not month:
            return

        # Clear previous chart
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        # Generate and embed chart
        data = team_feature.get_avg_precip_by_city(month)
        
        # Create figure
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(data['city'], data['precip'], color='steelblue')
        ax.set_title(f"Average Precipitation by City - {month}")
        ax.set_ylabel("Precipitation (mm)")
        ax.tick_params(axis='x', rotation=30)
        plt.tight_layout()

        # Embed in tkinter
        chart_canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Hook up dropdown
    month_dropdown.bind("<<ComboboxSelected>>", update_chart)

    return main_frame  # if parent app needs to do anything with it