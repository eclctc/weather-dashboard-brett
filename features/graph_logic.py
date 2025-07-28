# graph_logic.py
"""
Feature: Graph Logic
- Handles matplotlib integration and graph functionality for pollen data
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime
import tkinter as tk

class PollenChartGenerator:
    def __init__(self, data_file_path="data/pollen_atlanta_23_24.csv"):
        """Initialize the chart generator with data file path"""
        self.data_file_path = data_file_path
        self.data = None
        self.load_data()
    
    def load_data(self):
        """Load pollen data from CSV file"""
        try:
            self.data = pd.read_csv(self.data_file_path)
            # Convert date column to datetime
            self.data['date'] = pd.to_datetime(self.data['date'])
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def create_pollen_chart(self, chart_frame, chart_type="pollen"):
        """
        Create and display the requested chart type in the tkinter frame
        
        Args:
            chart_frame: The tkinter frame to display the chart in
            chart_type: Type of chart ("pollen", "temperature", "combined")
        """
        # Clear existing widgets in the frame
        for widget in chart_frame.winfo_children():
            widget.destroy()
        
        # Create matplotlib figure
        fig = Figure(figsize=(12, 8), dpi=100)
        
        if chart_type == "pollen":
            self._create_pollen_trends_chart(fig)
        elif chart_type == "temperature":
            self._create_temperature_placeholder(fig)
        elif chart_type == "combined":
            self._create_combined_chart(fig)
        
        # Create canvas and add to tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        return canvas
    
    def _create_pollen_trends_chart(self, fig):
        """Create pollen count trends chart"""
        if self.data is None:
            self._create_error_chart(fig, "No data available")
            return
        
        ax = fig.add_subplot(111)
        
        # Plot pollen counts over time
        ax.plot(self.data['date'], self.data['Count.tree_pollen'], 
                label='Tree Pollen', linewidth=2, color='green', alpha=0.8)
        ax.plot(self.data['date'], self.data['Count.grass_pollen'], 
                label='Grass Pollen', linewidth=2, color='orange', alpha=0.8)
        ax.plot(self.data['date'], self.data['Count.weed_pollen'], 
                label='Weed Pollen', linewidth=2, color='red', alpha=0.8)
        
        # Customize the chart
        ax.set_title('Pollen Count Trends (2023-2024)', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Pollen Count', fontsize=12)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        fig.autofmt_xdate()
        
        # Add some styling
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('white')
        
        plt.tight_layout()
    
    def _create_temperature_placeholder(self, fig):
        """Create temperature trends chart (placeholder since no temp data in sample)"""
        ax = fig.add_subplot(111)
        
        # Since we don't have temperature data, create a placeholder
        dates = self.data['date'] if self.data is not None else pd.date_range('2023-01-01', '2024-12-31', freq='D')
        
        # Generate sample temperature data for demonstration
        np.random.seed(42)
        temps = 70 + 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365) + np.random.normal(0, 5, len(dates))
        
        ax.plot(dates, temps, color='blue', linewidth=2, alpha=0.7)
        ax.fill_between(dates, temps, alpha=0.3, color='lightblue')
        
        ax.set_title('Temperature Trends (Sample Data)', fontsize=16, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Temperature (°F)', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Format x-axis dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        fig.autofmt_xdate()
        
        ax.set_facecolor('#f8f9fa')
        fig.patch.set_facecolor('white')
        
        plt.tight_layout()
    
    def _create_combined_chart(self, fig):
        """Create combined pollen and temperature analysis"""
        if self.data is None:
            self._create_error_chart(fig, "No data available")
            return
        
        # Create subplots
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        
        # Top subplot: Pollen counts
        ax1.plot(self.data['date'], self.data['Count.tree_pollen'], 
                label='Tree Pollen', color='green', linewidth=2)
        ax1.plot(self.data['date'], self.data['Count.grass_pollen'], 
                label='Grass Pollen', color='orange', linewidth=2)
        ax1.plot(self.data['date'], self.data['Count.weed_pollen'], 
                label='Weed Pollen', color='red', linewidth=2)
        
        ax1.set_title('Combined Weather & Pollen Analysis', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Pollen Count', fontsize=12)
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        ax1.set_facecolor('#f8f9fa')
        
        # Bottom subplot: Top species breakdown (pie chart)
        # Get average counts for top tree species
        tree_species = [
            'Species.Tree.Oak', 'Species.Tree.Cypress / Juniper / Cedar',
            'Species.Tree.Mulberry', 'Species.Tree.Pine', 'Species.Tree.Elm'
        ]
        
        species_data = []
        species_labels = []
        for species in tree_species:
            if species in self.data.columns:
                avg_count = self.data[species].mean()
                if avg_count > 0:
                    species_data.append(avg_count)
                    species_labels.append(species.split('.')[-1])  # Get just the species name
        
        if species_data:
            ax2.pie(species_data, labels=species_labels, autopct='%1.1f%%', startangle=90)
            ax2.set_title('Average Tree Species Distribution', fontsize=14)
        else:
            ax2.text(0.5, 0.5, 'No species data available', 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax2.transAxes, fontsize=12)
        
        fig.patch.set_facecolor('white')
        plt.tight_layout()
    
    def _create_error_chart(self, fig, error_message):
        """Create an error message chart"""
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, error_message, 
                horizontalalignment='center', verticalalignment='center',
                transform=ax.transAxes, fontsize=14, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.5))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        fig.patch.set_facecolor('white')
    
    def get_date_range_options(self):
        """Get available date range options for filtering"""
        if self.data is None:
            return []
        
        min_date = self.data['date'].min()
        max_date = self.data['date'].max()
        
        return {
            'full': (min_date, max_date),
            '2023': (datetime(2023, 1, 1), datetime(2023, 12, 31)),
            '2024': (datetime(2024, 1, 1), datetime(2024, 12, 31)),
            'spring_2023': (datetime(2023, 3, 1), datetime(2023, 5, 31)),
            'spring_2024': (datetime(2024, 3, 1), datetime(2024, 5, 31))
        }
    
    def filter_data_by_date(self, start_date, end_date):
        """Filter data by date range"""
        if self.data is None:
            return
        
        mask = (self.data['date'] >= start_date) & (self.data['date'] <= end_date)
        return self.data.loc[mask]

# Global instance for use in the view
chart_generator = PollenChartGenerator()

def chart_data(chart_frame, chart_type="pollen"):
    """
    Main function called from the view to generate charts
    
    Args:
        chart_frame: The tkinter frame to display the chart in
        chart_type: Type of chart to generate ("pollen", "temperature", "combined")
    """
    return chart_generator.create_pollen_chart(chart_frame, chart_type)