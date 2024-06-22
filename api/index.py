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

print('login')

no = "+918839000041"
pas = "Happy123$"
ck = "N7RD0Ydol8qBNE22SMffcT3FXpMa"
cs = "OfE3Hxw4QBAj7jSbrYsM5V01EQYa"

client = NeoAPI(consumer_key=ck, consumer_secret=cs, environment='prod',
                access_token=None, neo_fin_key=None)
client.login(mobilenumber=no, password=pas)


@app.route('/')
def home():
    return 'Hello'

@app.route('/otp')
def about():
    data = request.json
    otp = data.get('otp')
    token=otp
    client.session_2fa(OTP=token)
    client.scrip_master()
    return 'About'

if __name__ == '__main__':
    app.run(debug=True)