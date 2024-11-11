import requests
from django.core.cache import cache
from tkinter import *
import math
import os
from datetime import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'weather_app_backend.settings'
from django.core.cache import cache

import re

API_KEY_OPENWEATHERMAP = "b8ca77e6ba27170bfd7dbd6df8808da8"
WEATHER_API_URL_OPENWEATHERMAP = "https://api.openweathermap.org/data/2.5/weather"

API_KEY_WEATHERBIT = "6d754a69848b437a8a81a96d565797c7"
WEATHER_API_URL_WEATHERBIT = "https://api.weatherbit.io/v2.0/forecast/daily"


def generate_cache_key(city=None, latitude=None, longitude=None):
    if city:
        key = f"weather_{city}"
    else:
        key = f"weather_{latitude}_{longitude}"
    return re.sub(r'[^a-zA-Z0-9_]', '_', key)


def cache_weather_data(key, data, timeout=300):
    cache.set(key, data, timeout=timeout)


def fetch_weather_from_api(city=None, latitude=None, longitude=None):
    params = {"appid": API_KEY_OPENWEATHERMAP, "units": "metric"}
    if city:
        params["q"] = city
    else:
        params["lat"] = latitude
        params["lon"] = longitude

    response = requests.get(WEATHER_API_URL_OPENWEATHERMAP, params=params)

    # Check if the response status code is not 200
    if response.status_code != 200:
        raise Exception(f"Error fetching weather data: {response.status_code} - {response.reason}")
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


def fetch_weather_forecast(city=None, lat=None, lon=None, days=1):
    if not city and not (lat and lon):
        raise ValueError("Please provide either a city or latitude and longitude.")

    params = {"days": days, "key": API_KEY_WEATHERBIT}
    if city:
        params["city"] = city
    elif lat and lon:
        params["lat"] = lat
        params["lon"] = lon

    # Make the request to the Weatherbit API
    response = requests.get(WEATHER_API_URL_WEATHERBIT, params=params)

    # Check if the response status code is not 200, and raise an exception if so
    if response.status_code != 200:
        raise Exception(f"Error fetching weather data: {response.status_code} - {response.reason}")

    # Parse the response JSON data
    data = response.json()

    # Extract the date, max temp, and min temp for each day
    forecast_data = [
        {
            "date": day["datetime"],
            "max_temp": int(day["max_temp"]),
            "min_temp": int(day["min_temp"])
        }
        for day in data["data"]
    ]

    return forecast_data

