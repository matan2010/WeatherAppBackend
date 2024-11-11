"""
URL configuration for weather_app_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path
from .views import weather_views  # Import from views.weather_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', weather_views.weather_post, name='weather_post'),
    path('weather/<str:city>/', weather_views.weather_by_city, name='weather_by_city'),
    path('weather/coordinates/<str:latitude>/<str:longitude>/', weather_views.weather_by_coordinates,
         name='weather_by_coordinates'),
    path('forecast/', weather_views.weather_forecast, name='weather_forecast'),
]
