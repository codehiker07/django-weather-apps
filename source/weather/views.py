from django.shortcuts import render, HttpResponse
import requests
from bs4 import BeautifulSoup as bs

def get_weather_data(city):
    city = city.replace(' ', '+')
    url = f'https://www.google.com/search?q=weather+of+{city}'
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.9"
    session = requests.Session()
    session.headers['user-agent'] = USER_AGENT
    session.headers['accept-language'] = LANGUAGE
    response = session.get(url)
    soup = bs(response.text, 'html.parser')

    # Extract Region
    results = {}
    results['region'] = soup.find('span', attrs= {'class' : 'BBwThe'}).text
    results['daytime'] = soup.find('div', attrs= {'id' : 'wob_dts'}).text
    results['weather'] = soup.find('span', attrs= {'id' : 'wob_dc'}).text
    results['temp'] = soup.find('span', attrs= {'id' : 'wob_tm'}).text
    results['precipitation'] = soup.find('span', attrs= {'id' : 'wob_pp'}).text
    results['humidity'] = soup.find('span', attrs= {'id' : 'wob_hm'}).text
    results['wind'] = soup.find('span', attrs= {'id' : 'wob_ws'}).text
    # print(region, daytime, weather, temp, precipitation, humidity, wind)
    # print(results)
    return results
# Create your views here.

def home_view(request):
    if request.method == "GET" and 'city' in request.GET:
        city = request.GET.get('city')
        results = get_weather_data(city)
        context = {'results' : results}

    else:
        context = {}

    return render(request, 'weather/home.html', context)
