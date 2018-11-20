# Foodie web service

## Saraann Stanway, Srihari Shankar, Sam Azouzi, Heman Gandhi

## How to use the client

Send a get request: `http://localhost:5000/?address=<the address here>`.
This will geocode the address and then query zomato to grab nearby restaurants.
You should see a JSON object with the key `restaurants` that has a list of restaurants as
the value.

## Issues

Reading JSON is irritating.

## Libraries used

We run the service through [Flask](http://flask.pocoo.org/), python's simple web server library.
We use the [requests](http://docs.python-requests.org/en/master/) library to query the relevant APIs.

## How to start the service

```sh
pip install -r requirements.txt
python run.py
```

## Where are the keys

Lines 8 and 9 of run.py: they are just global variables.
