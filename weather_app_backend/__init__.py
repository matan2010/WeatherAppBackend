import requests
from tkinter import *
import math

city_name = "London"
api_key = "b8ca77e6ba27170bfd7dbd6df8808da8"
lat = 33.44
lon = -94.04


def get_weather(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url).json()
    print(response)


# get_weather(api_key,lat, lon)


def get_weather1(api_key, city_name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"
    response = requests.get(url).json()
    print(response)


#get_weather1(api_key, city_name)
