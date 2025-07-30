import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class PollenPredictor:
    def __init__(self, data_path='data/merged_pollen_weather_data.csv'):
        self.data_path = data_path
        self.models = {}
        self.scalers = {}
        self.pollen_types = ['Count.tree_pollen', 'Count.grass_pollen', 'Count.weed_pollen']
        self.feature_columns = ['temp', 'min_temp', 'max_temp', 'precip', 'wind_spd']
        self.data = None
        
    def load_and_prepare_data(self):
        """Load and prepare the data for modeling"""
        self.data = pd.read_csv(self.data_path)
        self.data['date'] = pd.to_datetime(self.data['date'])
        
        # Add seasonal features
        self.data['day_of_year'] = self.data['date'].dt.dayofyear
        self.data['month'] = self.data['date'].dt.month
        
        # Extended feature set including seasonal info
        self.feature_columns_extended = self.feature_columns + ['day_of_year', 'month']
        
        return self.data
    
    def train_models(self):
        """Train linear regression models for each pollen type"""
        if self.data is None:
            self.load_and_prepare_data()
        
        # Remove rows with missing values
        clean_data = self.data.dropna(subset=self.pollen_types + self.feature_columns_extended)
        
        X = clean_data[self.feature_columns_extended]
        
        for pollen_type in self.pollen_types:
            y = clean_data[pollen_type]
            
            # Scale features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Train model
            model = LinearRegression()
            model.fit(X_scaled, y)
            
            # Store model and scaler
            self.models[pollen_type] = model
            self.scalers[pollen_type] = scaler
    
    def get_historical_weather_pattern(self, target_date):
        """Get historical weather pattern for similar dates"""
        if self.data is None:
            self.load_and_prepare_data()
        
        target_day_of_year = target_date.timetuple().tm_yday
        target_month = target_date.month
        
        # Find similar dates (within 7 days of the same day of year)
        similar_dates = self.data[
            (abs(self.data['day_of_year'] - target_day_of_year) <= 7) |
            (abs(self.data['day_of_year'] - target_day_of_year) >= 358)  # Handle year boundary
        ]
        
        if len(similar_dates) > 0:
            # Use median values for similar dates
            return {
                'temp': similar_dates['temp'].median(),
                'min_temp': similar_dates['min_temp'].median(),
                'max_temp': similar_dates['max_temp'].median(),
                'precip': similar_dates['precip'].median(),
                'wind_spd': similar_dates['wind_spd'].median(),
                'day_of_year': target_day_of_year,
                'month': target_month
            }
        else:
            # Fallback to overall medians
            return {
                'temp': self.data['temp'].median(),
                'min_temp': self.data['min_temp'].median(),
                'max_temp': self.data['max_temp'].median(),
                'precip': self.data['precip'].median(),
                'wind_spd': self.data['wind_spd'].median(),
                'day_of_year': target_day_of_year,
                'month': target_month
            }
    
    def predict_pollen(self, weather_data):
        """Predict pollen counts based on weather data"""
        if not self.models:
            self.train_models()
        
        predictions = {}
        
        # Prepare feature vector
        features = np.array([[
            weather_data['temp'],
            weather_data['min_temp'],
            weather_data['max_temp'],
            weather_data['precip'],
            weather_data['wind_spd'],
            weather_data['day_of_year'],
            weather_data['month']
        ]])
        
        for pollen_type in self.pollen_types:
            # Scale features
            features_scaled = self.scalers[pollen_type].transform(features)
            
            # Make prediction
            prediction = self.models[pollen_type].predict(features_scaled)[0]
            
            # Ensure non-negative prediction
            prediction = max(0, prediction)
            
            predictions[pollen_type] = round(prediction, 1)
        
        return predictions
    
    def get_risk_level(self, pollen_count, pollen_type):
        """Convert pollen count to risk level based on typical thresholds"""
        if 'tree' in pollen_type.lower():
            if pollen_count <= 14:
                return 'Low'
            elif pollen_count <= 95:
                return 'Moderate'
            elif pollen_count <= 1499:
                return 'High'
            else:
                return 'Very High'
        elif 'grass' in pollen_type.lower():
            if pollen_count <= 9:
                return 'Low'
            elif pollen_count <= 49:
                return 'Moderate'
            elif pollen_count <= 199:
                return 'High'
            else:
                return 'Very High'
        elif 'weed' in pollen_type.lower():
            if pollen_count <= 9:
                return 'Low'
            elif pollen_count <= 49:
                return 'Moderate'
            elif pollen_count <= 199:
                return 'High'
            else:
                return 'Very High'
        return 'Unknown'
    
    def get_daily_forecast(self, target_date=None):
        """Get pollen forecast for a specific date"""
        if target_date is None:
            target_date = datetime.now().date()
        elif isinstance(target_date, str):
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        
        weather_data = self.get_historical_weather_pattern(target_date)
        predictions = self.predict_pollen(weather_data)
        
        forecast = {
            'date': target_date.strftime('%Y-%m-%d'),
            'day_name': target_date.strftime('%A'),
            'predictions': {}
        }
        
        for pollen_type, count in predictions.items():
            clean_name = pollen_type.replace('Count.', '').replace('_', ' ').title()
            risk_level = self.get_risk_level(count, pollen_type)
            
            forecast['predictions'][clean_name] = {
                'count': count,
                'risk_level': risk_level
            }
        
        return forecast
    
    def get_three_day_forecast(self, start_date=None):
        """Get 3-day pollen forecast"""
        if start_date is None:
            start_date = datetime.now().date()
            start_date = start_date + timedelta(days=1)

        elif isinstance(start_date, str):
            start_date = start_date + timedelta(days=1)
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            
        forecasts = []
        
        for i in range(3):
            forecast_date = start_date + timedelta(days=i)
            forecast = self.get_daily_forecast(forecast_date)
            forecasts.append(forecast)
        
        return forecasts