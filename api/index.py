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
    if request.is_json:
        data = request.get_json()
        otp = data.get('myotp')
        if otp:
            try:
                token = int(otp)
                # Assuming client is a pre-configured client instance
                client.session_2fa(OTP=token)
                client.scrip_master()
                return jsonify({'message': 'OTP processed successfully'}), 200
            except ValueError:
                return jsonify({'error': 'OTP must be an integer'}), 400
        else:
            return jsonify({'error': 'OTP not provided'}), 400
    else:
        return jsonify({'error': 'Request must be JSON'}), 415

if __name__ == '__main__':
    app.run(debug=True)