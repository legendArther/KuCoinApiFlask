from flask import Flask, jsonify, request
import ccxt
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Your KuCoin API credentials loaded from environment variables
api_key = os.getenv('KUCOIN_API_KEY')
api_secret = os.getenv('KUCOIN_API_SECRET')
api_password = os.getenv('KUCOIN_API_PASSWORD')

# Initialize the KuCoin futures exchange
exchange = ccxt.kucoinfutures({
    'apiKey': api_key,
    'secret': api_secret,
    'password': api_password,
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
    close_position()
    # Extract action, symbol, and amount from the alert
    action = data.get('action')
    symbol = data.get('symbol')
    amount = data.get('amount')
    leverage = data.get('leverage', 1)

    try:
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

