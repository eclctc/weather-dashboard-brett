import unittest
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from views.dashboard_view import WeatherView


class TestWeatherViewChart(unittest.TestCase):

    def setUp(self):
        # Create the view with a dummy callback
        self.view = WeatherView(on_refresh_callback=lambda: None)

    def test_chart_exists(self):
        # Force layout updates
        self.view.main_window.update_idletasks()

        # Test that the figure and canvas are created and of correct type
        self.assertIsInstance(self.view.fig, Figure, "fig should be a matplotlib Figure instance")
        self.assertIsInstance(self.view.canvas, FigureCanvasTkAgg, "canvas should be a FigureCanvasTkAgg instance")

        # Now check that canvas is packed into a widget and visible
        canvas_widget = self.view.canvas.get_tk_widget()
        self.assertTrue(canvas_widget.winfo_ismapped(), "Canvas widget should be mapped (visible in the layout)")


    def tearDown(self):
        # Destroy the window after test to prevent hanging GUI
        self.view.main_window.destroy()


if __name__ == '__main__':
    unittest.main()
