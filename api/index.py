from flask import Flask, jsonify, request
import ccxt
#from dotenv import load_dotenv
#import os

# Load environment variables from .env file
#load_dotenv()
import uuid
import hmac
import hashlib
import base64
import time
import json
import requests

app = Flask(__name__)

KUCOIN_API_KEY = '6662b0fbb2f56f0001658fcb'
KUCOIN_API_SECRET = '5b3a97e7-538e-4cd5-aafe-991725ba9a23'
KUCOIN_API_PASSWORD = 'Qwerty123'
# Your KuCoin API credentials loaded from environment variables

#api_key = os.getenv('KUCOIN_API_KEY')
#api_secret = os.getenv('KUCOIN_API_SECRET')
#api_password = os.getenv('KUCOIN_API_PASSWORD')

# Initialize the KuCoin futures exchange
exchange = ccxt.kucoinfutures({
    'apiKey': KUCOIN_API_KEY,
    'secret': KUCOIN_API_SECRET,
    'password': KUCOIN_API_PASSWORD,
    'enableRateLimit': True,
})

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

    # Extract action, symbol, and amount from the alert
    action = data.get('action')
    symbol = data.get('symbol')
    amount = data.get('amount')
    leverage = data.get('leverage', 1)

    try:
        close_position()
        if action == 'buy':
            order = exchange.create_market_buy_order(symbol, amount, {'leverage': leverage})
        elif action == 'short':
            order = exchange.create_market_sell_order(symbol, amount, {'leverage': leverage})
        else:
            return jsonify({'error': 'Invalid action'}), 400

        return jsonify(order)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/kucoin/close', methods=['POST'])
def close_position():
    data = request.json
    symbol = data['symbol']

    try:
        # Fetch open positions
        positions = exchange.fetch_positions([symbol])
        
        for position in positions:
            if position['symbol'] == symbol and position['contracts'] > 0:
                side = 'sell' if position['side'] == 'long' else 'buy'
                amount = position['contracts']

                # Create order to close the position
                if side == 'sell':
                    order = exchange.create_market_sell_order(symbol, amount)
                else:
                    order = exchange.create_market_buy_order(symbol, amount)

                return jsonify(order)

        return jsonify({'error': 'No open position found for the given symbol'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
