#! /bin/bash

# setup environment parameters
export FLASK_APP='application.py'
export ORDERS_URL="localhost:5000/api"
export PRODUCTS_URL="localhost:7777/api"
export USERS_ADDRESSES_URL="localhost:8888/api"

# ready to run actual app
flask run --host=0.0.0.0 --port=9999
