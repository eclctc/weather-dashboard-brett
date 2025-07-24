# team_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from features import team_feature

def create_team_view(parent_frame, parent_view):
    """Create the team view content"""
    # Main container
    main_frame = ttk.Frame(parent_frame)
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Title
    title_label = ttk.Label(main_frame, 
                           text="Breakout Room 7 - Team Information", 
                           font=("Arial", 14, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Project info
    project_frame = ttk.LabelFrame(main_frame, text="Project Overview", padding=15)
    project_frame.pack(fill=X, pady=(0, 20))
    
    project_text = """
    Project: Atlanta Weather & Pollen Prediction System
    
    Objective: Develop a multi-output regression model to predict both temperature 
    and pollen count using comprehensive weather data.
    
    Data Sources:
    • Weather data with 35+ meteorological parameters
    • Pollen count data with species-specific breakdowns
    • Time period: 2023-2024 for robust training
    """
    
    project_label = ttk.Label(project_frame, text=project_text, justify=LEFT)
    project_label.pack(anchor=W)
    
    # Team members (placeholder)
    team_frame = ttk.LabelFrame(main_frame, text="Team Members", padding=15)
    team_frame.pack(fill=X, pady=(0, 20))
    
    # Create a simple team member display
    members_frame = ttk.Frame(team_frame)
    members_frame.pack(fill=X)
    
    member_label = ttk.Label(members_frame, 
                            text="Team members and roles will be displayed here", 
                            font=("Arial", 10, "italic"))
    member_label.pack()
    
    # Progress section
    progress_frame = ttk.LabelFrame(main_frame, text="Project Progress", padding=15)
    progress_frame.pack(fill=BOTH, expand=True)
    
    # Progress items
    progress_items = [
        ("Data Collection", "Complete", "success"),
        ("Data Analysis", "In Progress", "warning"),
        ("Model Development", "Planned", "secondary"),
        ("UI Implementation", "In Progress", "info"),
        ("Testing & Validation", "Planned", "secondary")
    ]
    
    for i, (task, status, style) in enumerate(progress_items):
        task_frame = ttk.Frame(progress_frame)
        task_frame.pack(fill=X, pady=5)
        
        task_label = ttk.Label(task_frame, text=f"{task}:", width=20, anchor=W)
        task_label.pack(side=LEFT)
        
        status_label = ttk.Label(task_frame, text=status, bootstyle=style)
        status_label.pack(side=LEFT, padx=10)
        
        # Add progress bar for visual appeal
        if status == "Complete":
            progress = 100
        elif status == "In Progress":
            progress = 60
        else:
            progress = 0
            
        progress_bar = ttk.Progressbar(task_frame, value=progress, length=200)
        progress_bar.pack(side=RIGHT, padx=10)