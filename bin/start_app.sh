#! /bin/bash

# setup environment parameters
export FLASK_APP='application.py'
export ORDERS_URL="http://192.168.1.156:5000/"
export PRODUCTS_URL="http://192.168.1.156:7777"
export USERS_ADDRESSES_URL="http://192.168.1.156:8888"

# ready to run actual app
flask run --host=0.0.0.0 --port=9999
