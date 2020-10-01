from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

import requests
# Create your views here.

api_key = '0a449e1e45978ade3b750d5380634444'


def index(request):

    base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='
    url = base_url + api_key

    err_msg = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
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
