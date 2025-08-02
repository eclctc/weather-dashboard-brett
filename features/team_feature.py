# features/team_feature.py

import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Fiscal months in order
FISCAL_MONTHS = [
    "July", "August", "September", "October", "November", "December",
    "January", "February", "March", "April", "May", "June"
]

MONTH_NAME_TO_NUM = {name: i for i, name in enumerate(FISCAL_MONTHS, start=7)}
for i in range(1, 7):
    MONTH_NAME_TO_NUM[FISCAL_MONTHS[i + 5]] = i  # Jan-Jun remapping

def get_avg_precip_by_city(selected_month, data_path='data/team_weather_data.csv'):
    # Load data
    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])

    # Convert month name to number
    month_num = MONTH_NAME_TO_NUM[selected_month]

    # Filter by month
    df_month = df[df['date'].dt.month == month_num]

    # Group by city and calculate average precipitation
    avg_precip = df_month.groupby('city')['precip'].mean().reset_index()

    return avg_precip
