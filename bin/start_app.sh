#! /bin/bash

# setup environment parameters
export FLASK_APP='application.py'
export ORDERS_URL="http://160.39.244.167:5000"
export PRODUCTS_URL="http://160.39.244.167:7777"
export USERS_ADDRESSES_URL="http://160.39.244.167:8888"

# ready to run actual app
flask run --host=0.0.0.0 --port=9999
