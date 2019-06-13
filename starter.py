import json
import os

from flask import Flask, request, Response

import apis.fetch_from_datastore as datastore_api
import apis.fetch_from_openweather as ow_api
import apis.predict as pred
from utils.cors import crossdomain

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/current", methods=['GET'])
@crossdomain(origin='*')
def get_current_data():
    """Get real-time data from IoT simulators"""
    resp = datastore_api.get_current_data()
    print('Current data: \n' + str(resp))
    return Response(json.dumps(resp), mimetype='application/json')


@app.route("/predict_from_city", methods=['GET'])
@crossdomain(origin='*')
def predict_from_city():
    """Predict future average temperature by passing in model name and city name"""
    model = request.args.get('model')
    city = request.args.get('city')
    if city not in datastore_api.get_current_data():
        resp = {'message': 'Failed to process request! ' + city + ' is not part of the iot simulation.'}
    else:
        current_temp = datastore_api.get_current_data().get(city)
        ext_weather_attr = ow_api.get_by_city(city)
        resp = pred.predict(model, ext_weather_attr)

        celsius = round(float(current_temp) + float(resp))
        fahrenheit = round((celsius * 9 / 5) + 32)

        resp = {
            'city': city,
            'model': model,
            'current_temp_in_celsius': round(float(current_temp)),
            'current_temp_in_fahrenheit': round((float(current_temp) * 9 / 5) + 32),
            'pred_temp_in_celsius': celsius,
            'pred_temp_in_fahrenheit': fahrenheit
        }

    return Response(json.dumps(resp), mimetype='application/json')


@app.route("/predict_from_values", methods=['GET'])
@crossdomain(origin='*')
def predict_from_values():
    """Predict future average temperature by passing in model name and model parameters"""
    model = request.args.get('model')
    temp_max = request.args.get('temp_max')
    temp_min = request.args.get('temp_min')
    pressure = request.args.get('pressure')
    humidity = request.args.get('humidity')
    data = {
        'temp_max': float(temp_max),
        'temp_min': float(temp_min),
        'pressure': float(pressure),
        'humidity': float(humidity)
    }
    resp = pred.predict(model, data)

    celsius = round(float(resp))
    fahrenheit = round((celsius * 9 / 5) + 32)

    resp = {
        'model': model,
        'pred_temp_in_celsius': celsius,
        'pred_temp_in_fahrenheit': fahrenheit
    }

    return Response(json.dumps(resp), mimetype='application/json')


if __name__ == "__main__":
    if os.environ.get('OW_API_KEY') is None or os.environ.get('DATASTORE_SERVICE_ACCOUNT') is None:
        print("Please set the required env variables OW_API_KEY and DATASTORE_SERVICE_ACCOUNT.")
        print("See the README.md for details.")
    else:
        app.run(debug=True, host='0.0.0.0')

