from flask import Flask, jsonify, request
import ccxt
from dotenv import load_dotenv
import os
import requests
import neo_api_client
from neo_api_client import NeoAPI

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
def init_app():
    # Example: Log in to an external service and store the session token
    print('ok')
    no = "+918839000041"
    pas = "Happy123$"
    ck = "N7RD0Ydol8qBNE22SMffcT3FXpMa"
    cs = "OfE3Hxw4QBAj7jSbrYsM5V01EQYa"

    client = NeoAPI(consumer_key=ck, consumer_secret=cs, environment='prod',
                    access_token=None, neo_fin_key=None)
    client.login(mobilenumber=no, password=pas)
init_app()

@app.route('/')
def home():
    return 'Hello'

@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__':
    app.run(debug=True)

