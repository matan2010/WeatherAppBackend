import requests
from django.core.cache import cache
from tkinter import *
import math

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'weather_app_backend.settings'

from django.core.cache import cache

import re

city_name = "London"
API_KEY = "b8ca77e6ba27170bfd7dbd6df8808da8"
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
lat = 33.44
lon = -94.04


def get_weather_by_city(api_key, city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(url).json()
    print(response)


def get_weather_by_coordinates(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url).json()
    print(response)


# get_weather(api_key,lat, lon)


# get_weather1(api_key, city_name)

def get_weather_data(city=None, latitude=None, longitude=None):
    if not city and not (latitude and longitude):
        raise ValueError("Please provide either a city or latitude and longitude.")
    cache_key = f"weather_{city or f'{latitude}_{longitude}'}"
    cache_key = re.sub(r'[^a-zA-Z0-9_]', '_', cache_key)  # Replace invalid characters with '_'

    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    params = {"appid": API_KEY, "units": "metric"}
    if city:
        params["q"] = city
    else:
        params["lat"] = latitude
        params["lon"] = longitude

    response = requests.get(WEATHER_API_URL, params=params)
    if response.status_code == 200:
        weather_data = response.json()
        normalized_data = {
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "condition": weather_data["weather"][0]["description"]
        }
        cache.set(cache_key, normalized_data, timeout=300)  # Cache for 5 minutes
        return normalized_data
    else:
        raise Exception("Unable to fetch weather data.")


a=get_weather_data("Tokyo")
print(a)
