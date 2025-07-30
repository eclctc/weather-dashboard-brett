import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from features.prediction_logic import PollenPredictor
from datetime import datetime
import threading

def create_prediction_view(parent_frame, parent_view):
    """Create the prediction view content"""
    # Initialize predictor
    predictor = PollenPredictor()
    
    # Main container
    main_frame = ttk.Frame(parent_frame)
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Title
    title_label = ttk.Label(main_frame, 
                           text="🌸 Pollen Forecast Dashboard", 
                           font=("Arial", 16, "bold"))
    title_label.pack(pady=(0, 20))
    
    # Status section
    status_frame = ttk.LabelFrame(main_frame, text="Model Status", padding=15)
    status_frame.pack(fill=X, pady=(0, 20))
    
    status_label = ttk.Label(status_frame, text="🔄 Loading prediction models...", 
                            font=("Arial", 10), bootstyle="info")
    status_label.pack()
    
    # Progress bar for loading
    progress = ttk.Progressbar(status_frame, mode='indeterminate', bootstyle="info")
    progress.pack(fill=X, pady=(10, 0))
    progress.start()
    
    # Create horizontal container for side-by-side layout
    forecast_container = ttk.Frame(main_frame)
    forecast_container.pack(fill=BOTH, expand=True)
    
    # Today's forecast section (left side)
    today_frame = ttk.LabelFrame(forecast_container, text="📅 Today's Pollen Forecast", padding=15)
    today_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
    
    # Create grid for today's pollen types
    today_content_frame = ttk.Frame(today_frame)
    today_content_frame.pack(fill=BOTH, expand=True)
    
    # Headers for today's forecast
    ttk.Label(today_content_frame, text="Pollen Type", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=W, padx=(0, 15))
    ttk.Label(today_content_frame, text="Count", font=("Arial", 10, "bold")).grid(row=0, column=1, sticky=W, padx=(0, 15))
    ttk.Label(today_content_frame, text="Risk Level", font=("Arial", 10, "bold")).grid(row=0, column=2, sticky=W, padx=(0, 15))
    ttk.Label(today_content_frame, text="Status", font=("Arial", 10, "bold")).grid(row=0, column=3, sticky=W)
    
    # Separator
    separator1 = ttk.Separator(today_content_frame, orient=HORIZONTAL)
    separator1.grid(row=1, column=0, columnspan=4, sticky=EW, pady=10)
    
    # Today's pollen predictions (will be populated later)
    today_tree_count = ttk.Label(today_content_frame, text="--", font=("Arial", 10))
    today_tree_risk = ttk.Label(today_content_frame, text="--", font=("Arial", 10))
    today_tree_status = ttk.Label(today_content_frame, text="⚪", font=("Arial", 12))
    
    today_grass_count = ttk.Label(today_content_frame, text="--", font=("Arial", 10))
    today_grass_risk = ttk.Label(today_content_frame, text="--", font=("Arial", 10))
    today_grass_status = ttk.Label(today_content_frame, text="⚪", font=("Arial", 12))
    
    today_weed_count = ttk.Label(today_content_frame, text="--", font=("Arial", 10))
    today_weed_risk = ttk.Label(today_content_frame, text="--", font=("Arial", 10))
    today_weed_status = ttk.Label(today_content_frame, text="⚪", font=("Arial", 12))
    
    # Grid layout for today's predictions
    ttk.Label(today_content_frame, text="🌳 Tree Pollen").grid(row=2, column=0, sticky=W, padx=(0, 15), pady=5)
    today_tree_count.grid(row=2, column=1, sticky=W, padx=(0, 15), pady=5)
    today_tree_risk.grid(row=2, column=2, sticky=W, padx=(0, 15), pady=5)
    today_tree_status.grid(row=2, column=3, sticky=W, pady=5)
    
    ttk.Label(today_content_frame, text="🌾 Grass Pollen").grid(row=3, column=0, sticky=W, padx=(0, 15), pady=5)
    today_grass_count.grid(row=3, column=1, sticky=W, padx=(0, 15), pady=5)
    today_grass_risk.grid(row=3, column=2, sticky=W, padx=(0, 15), pady=5)
    today_grass_status.grid(row=3, column=3, sticky=W, pady=5)
    
    ttk.Label(today_content_frame, text="🌿 Weed Pollen").grid(row=4, column=0, sticky=W, padx=(0, 15), pady=5)
    today_weed_count.grid(row=4, column=1, sticky=W, padx=(0, 15), pady=5)
    today_weed_risk.grid(row=4, column=2, sticky=W, padx=(0, 15), pady=5)
    today_weed_status.grid(row=4, column=3, sticky=W, pady=5)
    
    # 3-Day forecast section (right side)
    forecast_frame = ttk.LabelFrame(forecast_container, text="📊 3-Day Pollen Forecast", padding=15)
    forecast_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))
    
    # Forecast display with scrollable text
    forecast_text = ttk.Text(forecast_frame, height=12, wrap=WORD, font=("Arial", 10))
    forecast_scrollbar = ttk.Scrollbar(forecast_frame, orient=VERTICAL, command=forecast_text.yview)
    forecast_text.configure(yscrollcommand=forecast_scrollbar.set)
    
    forecast_text.pack(side=LEFT, fill=BOTH, expand=True)
    forecast_scrollbar.pack(side=RIGHT, fill=Y)
    
    # Insert placeholder text
    forecast_text.insert("1.0", "📈 3-Day pollen forecast will appear here...\n\n" +
                                "Predictions will include:\n" +
                                "• Daily pollen counts for Tree, Grass, and Weed\n" +
                                "• Risk levels (Low, Moderate, High, Very High)\n" +
                                "• Visual indicators and detailed forecasts\n\n" +
                                "⏳ Please wait while models are being trained...")
    forecast_text.config(state="disabled")
    
    def get_risk_emoji(risk_level):
        """Get emoji based on risk level"""
        risk_emojis = {
            'Low': '🟢',
            'Moderate': '🟡',
            'High': '🟠',
            'Very High': '🔴'
        }
        return risk_emojis.get(risk_level, '⚪')
    
    def update_today_display(forecast):
        """Update today's forecast display"""
        predictions = forecast['predictions']
        
        # Update tree pollen
        if 'Tree Pollen' in predictions:
            data = predictions['Tree Pollen']
            today_tree_count.config(text=f"{data['count']:.1f}")
            today_tree_risk.config(text=data['risk_level'])
            today_tree_status.config(text=get_risk_emoji(data['risk_level']))
        
        # Update grass pollen  
        if 'Grass Pollen' in predictions:
            data = predictions['Grass Pollen']
            today_grass_count.config(text=f"{data['count']:.1f}")
            today_grass_risk.config(text=data['risk_level'])
            today_grass_status.config(text=get_risk_emoji(data['risk_level']))
        
        # Update weed pollen
        if 'Weed Pollen' in predictions:
            data = predictions['Weed Pollen']
            today_weed_count.config(text=f"{data['count']:.1f}")
            today_weed_risk.config(text=data['risk_level'])
            today_weed_status.config(text=get_risk_emoji(data['risk_level']))
    
    def format_forecast_text(forecasts):
        """Format the 3-day forecast for text display"""
        text = "🌸 3-DAY POLLEN FORECAST\n"
        text += "=" * 50 + "\n\n"
        
        for i, forecast in enumerate(forecasts):
            text += f"📅 Day {i+1}: {forecast['day_name']}, {forecast['date']}\n"
            text += "-" * 40 + "\n"
            
            for pollen_type, data in forecast['predictions'].items():
                emoji = get_risk_emoji(data['risk_level'])
                text += f"{emoji} {pollen_type:15} | Count: {data['count']:6.1f} | Risk: {data['risk_level']}\n"
            
            text += "\n"
        
        text += "=" * 50 + "\n"
        text += "📊 Risk Levels: 🟢 Low | 🟡 Moderate | 🟠 High | 🔴 Very High\n\n"
        text += "📈 Model Information:\n"
        text += "• Model Type: Linear Regression\n"
        text += "• Features: Temperature, Min/Max Temp, Precipitation, Wind Speed, Seasonal Patterns\n"
        text += "• Pollen Types: Tree, Grass, Weed\n"
        text += "• Predictions based on historical weather patterns for similar dates"
        
        return text
    
    def load_predictions():
        """Load predictions in a separate thread"""
        try:
            # Train models
            predictor.train_models()
            
            # Get today's forecast
            today = datetime.now().date()
            today_forecast = predictor.get_daily_forecast(today)
            
            # Get 3-day forecast
            three_day_forecast = predictor.get_three_day_forecast(today)
            
            # Update GUI in main thread
            parent_frame.after(0, update_gui, today_forecast, three_day_forecast)
            
        except Exception as e:
            parent_frame.after(0, show_error, str(e))
    
    def update_gui(today_forecast, three_day_forecast):
        """Update the GUI with forecast data"""
        # Stop progress bar and update status
        progress.stop()
        progress.pack_forget()
        status_label.config(text="✅ Models loaded successfully! Displaying predictions...", 
                          bootstyle="success")
        
        # Update today's display
        update_today_display(today_forecast)
        
        # Update 3-day forecast text
        forecast_text.config(state="normal")
        forecast_text.delete("1.0", END)
        forecast_text.insert("1.0", format_forecast_text(three_day_forecast))
        forecast_text.config(state="disabled")
    
    def show_error(error_message):
        """Show error message"""
        progress.stop()
        progress.pack_forget()
        status_label.config(text=f"❌ Error: {error_message}", bootstyle="danger")
        
        # Update forecast text with error info
        forecast_text.config(state="normal")
        forecast_text.delete("1.0", END)
        forecast_text.insert("1.0", f"❌ Error loading pollen predictions:\n\n{error_message}\n\n" +
                                    "Please ensure:\n" +
                                    "• data/merged_pollen_weather_data.csv exists\n" +
                                    "• The file contains the required columns\n" +
                                    "• The data is properly formatted")
        forecast_text.config(state="disabled")
    
    # Start loading predictions in background thread
    thread = threading.Thread(target=load_predictions, daemon=True)
    thread.start()