#!venv/bin/python
#from xd import app, db
import requests

import os
from flask import Flask, request, jsonify
app = Flask(__name__)

geocode_key = "55f25fb5440fbf37dd545534ddd53ee5d43e2b2"
zomato_key = "05fb51eb0e4d27b795abe3910420f06a"

@app.route('/')
def restaurant():
    location = request.args.get('address')
    if location is None or location == '':
        return "Address parameter not provided", 400

    params = {'q': location, 'api_key': geocode_key}
    geocode = requests.get('https://api.geocod.io/v1.3/geocode', params)
    latitude = geocode.json().get('results', [{'location': dict()}])[0].get('location', dict()).get('lat')
    longitude = geocode.json().get('results', [{'location': dict()}])[0].get('location', dict()).get('lng')
    if latitude is None or longitude is None:
        err = geocode.json().get('error')
        if err is None:
            return "Geocode API failed us!",503
        return err, 400
    location = [latitude, longitude]

    params = {'lat':latitude, 'lon': longitude}
    header = {'user-key': zomato_key}
    restaurants = requests.get('https://developers.zomato.com/api/v2.1/geocode', params, headers=header)
    results_dict = {"restaurants":[]}
    restaurants = restaurants.json().get('nearby_restaurants')
    if restaurants is None:
        return "Zomato API failed us!", 503

    for restaurant in (i.get('restaurant') for i in restaurants):
        results_dict['restaurants'].append({'name':restaurant.get('name'),'address':restaurant.get('location').get('address'), 'cuisines':restaurant.get('cuisines'),'rating':restaurant.get('user_rating').get('aggregate_rating')})
    return jsonify(results_dict)

if __name__ == '__main__':
    app.run(debug=True)



