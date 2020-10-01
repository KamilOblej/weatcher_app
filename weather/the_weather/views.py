from django.shortcuts import render
from .models import City
from .forms import CityForm

import requests
# Create your views here.

api_key = '0a449e1e45978ade3b750d5380634444'


def index(request):

    base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='
    url = base_url + api_key

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    # print(weather_data)

    context = {'weather_data': weather_data, 'form': form}
    # print(context)

    return render(request, 'the_weather/weather.html', context)
