"""Services for querying IoT data from Google Cloud Datastore"""
import os

from google.cloud import datastore
from pycountry import countries


def get_city_full_name(city_name, country_name):
    try:
        country = countries.get(name=country_name).alpha_2
        city = city_name + ',' + country
        return city
    except AttributeError:
        print('ISO 3166 country code for ' + city_name + ' is not available in database')
        return city_name


def get_current_data():
    client = datastore.Client.from_service_account_json(os.environ['DATASTORE_SERVICE_ACCOUNT'])
    query = client.query(kind='CityEntity')
    entities = list(query.fetch())

    city_temp_dict = {}
    for i in range(len(entities)):
        name = entities[i]['name']
        if '-' in name:
            names = name.split('-')
            if len(names) == 2:
                city = get_city_full_name(names[1], names[0]).lower()
            elif len(names) == 3:
                city = get_city_full_name(names[2], names[0]).lower()
            else:
                city = names[-1].lower()
        else:
            city = name.lower()
        temp = entities[i]['avgTemperature']
        city_temp_dict[city] = temp
    return city_temp_dict


def get_city_key_dict():
    client = datastore.Client.from_service_account_json(os.environ['DATASTORE_SERVICE_ACCOUNT'])
    query = client.query(kind='CityEntity')
    entities = list(query.fetch())

    city_key_dict = {}
    for i in range(len(entities)):
        name = entities[i]['name']
        if '-' in name:
            names = name.split('-')
            if len(names) == 2:
                city = get_city_full_name(names[1], names[0]).lower()
            elif len(names) == 3:
                city = get_city_full_name(names[2], names[0]).lower()
            else:
                city = names[-1].lower()
        else:
            city = name.lower()
        city_key_dict[city] = entities[i].key
    return city_key_dict


def get_coord_key_dict():
    client = datastore.Client.from_service_account_json(os.environ['DATASTORE_SERVICE_ACCOUNT'])
    query = client.query(kind='CityEntity')
    entities = list(query.fetch())

    coord_key_dict = {}
    for i in range(len(entities)):
        lat = entities[i]['lat']
        lon = entities[i]['lng']
        coord_key_dict[(lat, lon)] = entities[i].key
    return coord_key_dict


def get_temp(dict, key):
    client = datastore.Client.from_service_account_json(os.environ['DATASTORE_SERVICE_ACCOUNT'])
    query = client.query(kind='CityEntity')
    query.add_filter('__key__', '=', dict[key])
    entity = list(query.fetch())
    temp = entity[0]['avgTemperature']
    return temp
