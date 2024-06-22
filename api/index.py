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

@app.before_first_request
def setup_server_session():
    # Example: Log in to an external service and store the session token
    
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

@app.route('/about')
def about():
    return 'About'

@app.route('/kucoin/<symbol>')
def kucoin_price(symbol):
    url = f'https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        price = data['data']['price']
        return jsonify({
            'symbol': symbol,
            'price': price
        })
    else:
        return jsonify({
            'error': 'Failed to fetch data from KuCoin API'
        }), response.status_code

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    close_position()
    # Extract action, symbol, and amount from the alert
    action = data.get('action')
    symbol = data.get('symbol')
    amount = data.get('amount')
    leverage = data.get('leverage', 1)

@app.route('/kucoin/close', methods=['POST'])
def close_position():
    data = request.json
    return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

