from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods, require_POST
from weather_app_backend.service.weather_service import get_weather_data, get_cached_weather_data, \
    fetch_weather_forecast

from django.views.decorators.csrf import csrf_exempt
import json


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def weather_post(request):
    try:
        data = json.loads(request.body)
        city = data.get('city')
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if city:
            weather_data = get_weather_data(city=city)
        elif latitude and longitude:
            weather_data = get_weather_data(latitude=latitude, longitude=longitude)
        else:
            return HttpResponseBadRequest("Please provide either a city name or coordinates.")

        return JsonResponse(weather_data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def weather_by_city(request, city):
    try:
        cached_data = get_cached_weather_data(city)
        if isinstance(cached_data, str):  # If not cached, return message as Json
            return JsonResponse({"message": cached_data}, status=404)
        return JsonResponse(cached_data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@require_http_methods(["GET"])
def weather_by_coordinates(request, latitude, longitude):
    try:
        latitude = float(latitude)
        longitude = float(longitude)

        if not (latitude and longitude):
            return HttpResponseBadRequest("Please provide both latitude and longitude.")

        weather_data = get_weather_data(latitude=latitude, longitude=longitude)
        return JsonResponse(weather_data)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required
@csrf_exempt
@require_POST
def weather_forecast(request):
    try:
        # Parse JSON body
        data = json.loads(request.body)
        city = data.get('city')
        lat = data.get('lat')
        lon = data.get('lon')
        days = data.get('days')

        # Call the function and fetch forecast data
        forecast = fetch_weather_forecast(city=city, lat=lat, lon=lon, days=days)
        return JsonResponse({"forecast": forecast}, status=200)

    except ValueError as ve:
        return JsonResponse({"error": str(ve)}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

