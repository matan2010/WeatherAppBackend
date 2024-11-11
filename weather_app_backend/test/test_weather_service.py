import unittest
from unittest.mock import patch, MagicMock
from weather_app_backend.service.weather_service import (
    generate_cache_key,
    cache_weather_data,
    fetch_weather_from_api,
    normalize_weather_data,
    get_weather_data,
    get_cached_weather_data,
    fetch_weather_forecast
)


class TestWeatherService(unittest.TestCase):
    def test_generate_cache_key_with_city(self):
        key = generate_cache_key(city="London")
        self.assertEqual(key, "weather_London")

    def test_generate_cache_key_with_coordinates(self):
        key = generate_cache_key(latitude=51.5074, longitude=-0.1278)
        self.assertEqual(key, "weather_51_5074__0_1278")

    @patch('weather_app_backend.service.weather_service.cache.set')
    def test_cache_weather_data(self, mock_cache_set):
        cache_weather_data("weather_London", {"temp": 25}, timeout=300)
        mock_cache_set.assert_called_once_with("weather_London", {"temp": 25}, timeout=300)

    @patch('weather_app_backend.service.weather_service.requests.get')
    def test_fetch_weather_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 20.5, "humidity": 60},
            "weather": [{"description": "clear sky"}]
        }
        mock_get.return_value = mock_response

        data = fetch_weather_from_api(city="London")
        self.assertEqual(data["main"]["temp"], 20.5)

    @patch('weather_app_backend.service.weather_service.requests.get')
    def test_fetch_weather_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            fetch_weather_from_api(city="UnknownCity")
        self.assertIn("Error fetching weather data: 404 - Not Found", str(context.exception))

    def test_normalize_weather_data(self):
        data = {
            "main": {"temp": 20.9, "humidity": 60},
            "weather": [{"description": "clear sky"}]
        }
        normalized_data = normalize_weather_data(data)
        self.assertEqual(normalized_data["temperature"], 20)
        self.assertEqual(normalized_data["humidity"], 60)
        self.assertEqual(normalized_data["condition"], "clear sky")

    @patch('weather_app_backend.service.weather_service.cache.get')
    @patch('weather_app_backend.service.weather_service.cache.set')
    @patch('weather_app_backend.service.weather_service.requests.get')
    def test_get_weather_data_without_cache(self, mock_requests_get, mock_cache_set, mock_cache_get):
        mock_cache_get.return_value = None  # No cached data

        # Mock response with the necessary 'coord' key
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 20.5, "humidity": 60},
            "weather": [{"description": "clear sky"}],
            "coord": {"lat": 51.5074, "lon": -0.1278}  # Add 'coord' with 'lat' and 'lon'
        }
        mock_requests_get.return_value = mock_response

        data = get_weather_data(city="London")
        self.assertEqual(data["temperature"], 20)
        mock_cache_set.assert_called()

    @patch('weather_app_backend.service.weather_service.cache.get')
    def test_get_cached_weather_data_exists(self, mock_get):
        mock_get.return_value = {"temperature": 20, "humidity": 60, "condition": "clear sky"}
        data = get_cached_weather_data(city="London")
        self.assertEqual(data["temperature"], 20)

    @patch('weather_app_backend.service.weather_service.cache.get')
    def test_get_cached_weather_data_not_exists(self, mock_get):
        mock_get.return_value = None
        data = get_cached_weather_data(city="UnknownCity")
        self.assertEqual(data, "Weather data does not exist in cache.")

    @patch(
        "weather_app_backend.service.weather_service.requests.get")
    def test_fetch_weather_forecast_city(self, mock_get):
        # Mock response for a successful API call
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"datetime": "2024-11-12", "max_temp": 25, "min_temp": 15},
                {"datetime": "2024-11-13", "max_temp": 23, "min_temp": 14}
            ]
        }
        mock_get.return_value = mock_response

        # Call the function with a city parameter
        result = fetch_weather_forecast(city="New York", days=2)

        # Check that the returned forecast data is correct
        expected_result = [
            {"date": "2024-11-12", "max_temp": 25, "min_temp": 15},
            {"date": "2024-11-13", "max_temp": 23, "min_temp": 14}
        ]
        self.assertEqual(result, expected_result)

    @patch(
        "weather_app_backend.service.weather_service.requests.get")
    def test_fetch_weather_forecast_lat_lon(self, mock_get):
        # Mock response for a successful API call
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"datetime": "2024-11-12", "max_temp": 20, "min_temp": 10}
            ]
        }
        mock_get.return_value = mock_response

        # Call the function with latitude and longitude parameters
        result = fetch_weather_forecast(lat=40.7128, lon=-74.0060, days=1)

        # Check that the returned forecast data is correct
        expected_result = [
            {"date": "2024-11-12", "max_temp": 20, "min_temp": 10}
        ]
        self.assertEqual(result, expected_result)

    def test_fetch_weather_forecast_missing_parameters(self):
        # Test that a ValueError is raised if neither city nor lat/lon is provided
        with self.assertRaises(ValueError):
            fetch_weather_forecast(days=1)

    @patch(
        "weather_app_backend.service.weather_service.requests.get")
    def test_fetch_weather_forecast_api_error(self, mock_get):
        # Mock response for an API error (e.g., status code 404)
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.reason = "Not Found"
        mock_get.return_value = mock_response

        # Test that an exception is raised with the correct message
        with self.assertRaises(Exception) as context:
            fetch_weather_forecast(city="NonExistentCity", days=1)
        self.assertEqual(str(context.exception), "Error fetching weather data: 404 - Not Found")
