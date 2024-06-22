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
    try:
        data = request.json  # Ensure you are getting JSON data
        otp = data.get('myotp')
        token = otp

        # Set the correct headers and payload for session_2fa
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'OTP': otp
        }

        # Assuming client is an instance of a class that has session_2fa and scrip_master methods
        response = client.session_2fa(payload, headers=headers)

        if response.status_code == 200:
            client.scrip_master()
            return 'About'
        else:
            return f"Error: {response.text}", response.status_code
    except Exception as e:
        return str(e), 500

    
@app.route('/buy')
def buy():
    order_response = client.place_order(
        exchange_segment='NSE',  # Example: National Stock Exchange Futures & Options segment
        product='MIS',  # Specify that it's an options order
        price='',  # Price at which you want to buy/sell the option
        order_type='MKT',  # Order type, e.g., 'LIMIT', 'MARKET'
        quantity= '1',  # Quantity of the options contract
        validity='DAY',  # Order validity, e.g., 'DAY', 'IOC'
        trading_symbol='TATASTEEL-EQ',  # Example trading symbol for the option
        transaction_type='B'  # Transaction type: 'BUY' or 'SELL'
    )

    print("Order Response:", order_response)
if __name__ == '__main__':
    app.run(debug=True)