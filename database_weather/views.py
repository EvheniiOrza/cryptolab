import requests
from django.shortcuts import render
from django.core.cache import cache
from datetime import datetime

API_KEY = 'a7391429b50609e2033b95dc5d5d1d5a'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'


def get_weather(request):
    city = request.GET.get('city', 'Kyiv')
    cache_key = f"weather_{city.lower()}"
    weather_data = cache.get(cache_key)

    if not weather_data:
        response = requests.get(BASE_URL, params={
            'q': city,
            'appid': API_KEY,
            'units': 'metric'
        })
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data.get('name', 'N/A'),
                'temperature': data['main'].get('temp', 'N/A'),
                'feels_like': data['main'].get('feels_like', 'N/A'),
                'description': data['weather'][0].get('description', 'N/A').capitalize(),
                'humidity': data['main'].get('humidity', 'N/A'),
                'pressure': data['main'].get('pressure', 'N/A'),
                'wind_speed': data['wind'].get('speed', 'N/A'),
                'wind_direction': data['wind'].get('deg', 'N/A'),
                'sunrise': datetime.utcfromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S'),
                'sunset': datetime.utcfromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S'),
                'icon': data['weather'][0].get('icon', '01d')
            }
            cache.set(cache_key, weather_data, 1800)
        else:
            weather_data = {'error': 'City not found'}

    return render(request, 'weather.html', {'weather': weather_data})
