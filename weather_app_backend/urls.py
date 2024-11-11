from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, re_path
from .views import weather_views  # Import from views.weather_views
from . import user_views

urlpatterns = [
    path('login/', user_views.weather_login, name='weather_login'),
    path('signup/', user_views.signup, name='signup'),
    path('weather/', weather_views.weather_post, name='weather_post'),
    path('weather/<str:city>/', weather_views.weather_by_city, name='weather_by_city'),
    path('weather/coordinates/<str:latitude>/<str:longitude>/', weather_views.weather_by_coordinates,
         name='weather_by_coordinates'),
]
