from django.shortcuts import render

import requests
# Create your views here.


def index(request):
    city = 'Warsaw'
    api_key = '0a449e1e45978ade3b750d5380634444'
    base_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='
    url = base_url + api_key

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    context = {'city_weather': city_weather}
    print(context)

    return render(request, 'the_weather/weather.html', context)
