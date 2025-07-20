import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import requests
from unittest.mock import patch, Mock
from models.weather_model import WeatherModel

# ---------- Test: validate_city_name ----------
def test_validate_city_name():
    wm = WeatherModel(api_key="dummy")
    assert wm.validate_city_name("New York") is True
    assert wm.validate_city_name("   ") is False
    assert wm.validate_city_name("") is False

# ---------- Test: fetch_weather_data (success) ----------
@patch('models.weather_model.requests.get')
def test_fetch_weather_data_success(mock_get):
    dummy_response = {
        "dt": 1721455200,  # Example timestamp
        "main": {
            "temp": 75.5,
            "humidity": 60
        },
        "weather": [
            {"description": "clear sky"}
        ]
    }

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = dummy_response
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    wm = WeatherModel(api_key="dummy")
    data, source = wm.fetch_weather_data("Miami")
    
    assert data is not None
    assert data["temp"] == 75.5
    assert data["description"] == "clear sky"
    assert data["humidity"] == 60
    assert "Open Weather API" in source

# ---------- Test: fetch_weather_data (timeout) ----------
@patch('models.weather_model.requests.get', side_effect=requests.exceptions.Timeout)
def test_fetch_weather_data_timeout(mock_get):
    wm = WeatherModel(api_key="dummy")
    data, source = wm.fetch_weather_data("Chicago")
    
    assert data is None
    assert "timed out" in source

# ---------- Test: fetch_weather_data (HTTP error) ----------
@patch('models.weather_model.requests.get')
def test_fetch_weather_data_http_error(mock_get):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(response=Mock(status=404))
    mock_get.return_value = mock_response

    wm = WeatherModel(api_key="dummy")
    data, source = wm.fetch_weather_data("Atlantis")  # Invalid city for test

    assert data is None
