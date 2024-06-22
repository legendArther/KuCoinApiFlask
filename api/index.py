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
pas = "Happy123$$"
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
        data = request.json
        otp = data.get('myotp')
        token = otp
        #client.session_2fa(OTP=str(otp))
        return 'About'
    except Exception as e:
        print("Exception : %s\n" % e)
        return str(e)
    
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