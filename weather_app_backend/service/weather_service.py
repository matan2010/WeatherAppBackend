import requests
from django.core.cache import cache
from tkinter import *
import math
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'weather_app_backend.settings'
from django.core.cache import cache

import re

API_KEY = "b8ca77e6ba27170bfd7dbd6df8808da8"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"


def generate_cache_key(city=None, latitude=None, longitude=None):
    if city:
        key = f"weather_{city}"
    else:
        key = f"weather_{latitude}_{longitude}"
    return re.sub(r'[^a-zA-Z0-9_]', '_', key)


def cache_weather_data(key, data, timeout=300):
    cache.set(key, data, timeout=timeout)


def fetch_weather_from_api(city=None, latitude=None, longitude=None):
    params = {"appid": API_KEY, "units": "metric"}
    if city:
        params["q"] = city
    else:
        params["lat"] = latitude
        params["lon"] = longitude

    response = requests.get(WEATHER_API_URL, params=params)

    # Check if the response status code is not 200
    if response.status_code != 200:
        error_message = f"Error fetching weather data: {response.status_code} - {response.reason}"
        raise Exception(error_message)
    response.raise_for_status()
    return response.json()


def normalize_weather_data(data):
    temperature = data["main"]["temp"]
    integer_part = math.floor(temperature)
    return {
        "temperature": integer_part,
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"]
    }


def get_weather_data(city=None, latitude=None, longitude=None):
    if not city and not (latitude and longitude):
        raise ValueError("Please provide either a city or latitude and longitude.")

    # Define and sanitize the primary cache key
    primary_cache_key = generate_cache_key(city, latitude, longitude)

    # Check if data is cached
    cached_data = cache.get(primary_cache_key)
    if cached_data:
        return cached_data

    # Fetch and normalize data from API
    weather_data = fetch_weather_from_api(city, latitude, longitude)
    normalized_data = normalize_weather_data(weather_data)

    # Cache normalized data with both primary and alternate keys
    cache_weather_data(primary_cache_key, normalized_data)
    if city:
        coord_cache_key = generate_cache_key(latitude=weather_data['coord']['lat'],
                                             longitude=weather_data['coord']['lon'])
        cache_weather_data(coord_cache_key, normalized_data)
    else:
        city_cache_key = generate_cache_key(city=weather_data['name'])
        cache_weather_data(city_cache_key, normalized_data)

    return normalized_data


def get_cached_weather_data(city):
    cache_key = generate_cache_key(city)
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data  # Return cached weather data if found
    else:
        return "Weather data does not exist in cache."


b = get_weather_data("London")
print(b)
# print(a)


a = get_weather_data(latitude=51.5085, longitude=-0.1257)
print(a)

b = get_weather_data("London")
print(b)
# print(a)

# a = get_weather_data(latitude=35.6895, longitude=139.6917)
# print(a)

b = get_weather_data("Tokyo")
print(b)
k = get_cached_weather_data("Tokyo")
print(k)
