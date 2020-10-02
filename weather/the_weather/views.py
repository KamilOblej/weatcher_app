from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
from datetime import datetime

import requests
# Create your views here.

api_key = '0a449e1e45978ade3b750d5380634444'
base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='
url = base_url + api_key


def index(request):
    err_msg = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'Oh, Wrong city name!'
            else:
                err_msg = 'City already exist in the database!'

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

    context = {'weather_data': weather_data,
               'form': form,
               'err_msg': err_msg}
    # print(context)

    return render(request, 'the_weather/weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')


def get_back(request):
    return redirect('home')


def details(request, city_name):

    forecast_url = "https://api.openweathermap.org/data/2.5/onecall?lat=53.43&lon=14.55&exclude=hourly,minutely&units=metric&appid=" + api_key

    r = requests.get(url.format(city_name)).json()
    fr = requests.get(forecast_url.format(city_name)).json()

    lat = r['coord']['lat']
    lon = r['coord']['lon']

    city_weather = {
        'city': city_name,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
        'feels_like': r['main']['feels_like'],
        'temp_min': r['main']['temp_min'],
        'temp_max': r['main']['temp_max'],
        'humidity': r['main']['humidity'],
        'pressure': r['main']['pressure'],
        'wind_speed': r['wind']['speed'],
        'wind_deg': r['wind']['deg'],
    }

    weekly_forecast = []
    i = 0
    for days in range(6):
        i += 1
        day_forecast = {
            # 'date': fr['daily'][3]['dt'],
            'utc_date': datetime.utcfromtimestamp(fr['daily'][i]['dt']).strftime('%Y-%m-%d'),
            'icon': fr['daily'][i]['weather'][0]['icon'],
            'day_temperature': fr['daily'][i]['temp']['day'],
            'night_temperature': fr['daily'][0]['temp']['night'],
            'humidity': fr['daily'][i]['humidity'],
            'pressure': fr['daily'][i]['pressure'],
        }
        weekly_forecast.append(day_forecast)

    # forecast = {
    #     # 'date': fr['daily'][3]['dt'],
    #     'utc_date': datetime.utcfromtimestamp(fr['daily'][0]['dt']).strftime('%Y-%m-%d'),
    #     'icon': fr['daily'][0]['weather'][0]['icon'],
    #     'day_temperature': fr['daily'][0]['temp']['day'],
    #     'night_temperature': fr['daily'][0]['temp']['night'],
    #     'humidity': fr['daily'][0]['humidity'],
    #     'pressure': fr['daily'][0]['pressure'],
    # }

    context = {
        'city_weather': city_weather,
        'weekly_forecast': weekly_forecast,
    }
    return render(request, 'the_weather/details.html', context)
