from flask import Flask, jsonify
import requests # type: ignore

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)
