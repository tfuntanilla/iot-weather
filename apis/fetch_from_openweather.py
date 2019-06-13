"""Services for querying additional weather data"""

import os

import requests

API_ENDPOINT = 'http://api.openweathermap.org'
URL = API_ENDPOINT + '/data/2.5/weather'


def get_by_city(city_name):
    params = {'q': city_name, 'APPID': os.environ['OW_API_KEY'], 'units': 'metric'}
    req = requests.get(url=URL, params=params)
    resp = req.json()
    data = resp['main']
    del data['temp']
    return data

def get_by_lat_lon(lat, lon):
    params = {'lat': lat, 'lon': lon, 'APPID': os.environ['OW_API_KEY'], 'units': 'metric'}
    req = requests.get(url=URL, params=params)
    resp = req.json()
    data = resp['main']
    del data['temp']
    return data

