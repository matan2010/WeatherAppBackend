# weather/tasks.py
from celery import shared_task
from .service.weather_service import fetch_weather_from_api, normalize_weather_data, cache_weather_data, generate_cache_key


@shared_task
def refresh_weather_cache(city=None, latitude=None, longitude=None):
    try:
        weather_data = fetch_weather_from_api(city, latitude, longitude)
        normalized_data = normalize_weather_data(weather_data)
        cache_key = generate_cache_key(city, latitude, longitude)
        cache_weather_data(cache_key, normalized_data)
    except Exception as e:
        print(f"Error refreshing weather cache: {e}")