#!venv/bin/python

import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

geocode_key = "55f25fb5440fbf37dd545534ddd53ee5d43e2b2"
zomato_key = "05fb51eb0e4d27b795abe3910420f06a"

@app.route('/')
def restaurant():
    """The main (only) route: an address query param is expected."""
    location = request.args.get('address')
    #check for user mistake
    if location is None or location == '':
        return "Address parameter not provided", 400

    #try to geocode the location
    params = {'q': location, 'api_key': geocode_key}
    geocode = requests.get('https://api.geocod.io/v1.3/geocode', params)
    latitude = geocode.json().get('results', [{'location': dict()}])[0].get('location', dict()).get('lat')
    longitude = geocode.json().get('results', [{'location': dict()}])[0].get('location', dict()).get('lng')

    #Error case: geocoding failed.
    if latitude is None or longitude is None:
        err = geocode.json().get('error')
        #we assumed that if the API did not return an error, the API is down
        if err is None:
            return "Geocode API failed us!",503
        #otherwise, the error should be a user error (like an address that's not an address)
        #so we inform them.
        return err, 400
    location = [latitude, longitude]

    #zomoto query
    params = {'lat':latitude, 'lon': longitude}
    header = {'user-key': zomato_key}
    restaurants = requests.get('https://developers.zomato.com/api/v2.1/geocode', params, headers=header)
    results_dict = {"restaurants":[]}
    restaurants = restaurants.json().get('nearby_restaurants')
    #we assume that zomato would find something. Otherwise it's down.
    if restaurants is None:
        return "Zomato API failed us!", 503

    #re-format the data to the spec
    for restaurant in (i.get('restaurant') for i in restaurants):
        results_dict['restaurants'].append({
            'name':restaurant.get('name'),
            'address':restaurant.get('location').get('address'),
            'cuisines':restaurant.get('cuisines'),
            'rating':restaurant.get('user_rating').get('aggregate_rating')
        })
    return jsonify(results_dict)

if __name__ == '__main__':
    app.run(debug=True)



