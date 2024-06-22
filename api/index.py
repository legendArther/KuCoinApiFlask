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
def otp():
    try:
        myotp = request.args.get('myotp')
        client.session_2fa(OTP=str(myotp))
        return myotp
    except Exception as e:
        print("Exception : %s\n" % e)
        return str(e)
    
@app.route('/buy')
def buy():
    try:
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
        # Check the status of the order response
        if order_response['stat'] != 'Ok':
            return jsonify(order_response), 400  # Returning a 400 Bad Request with the error details

        return jsonify({'message': 'Order placed successfully'}), 200

    except Exception as e:
        error_message = f"Exception on /buy: {str(e)}"
        print(error_message)
        return jsonify({'error': error_message}), 500  # Returning a 500 Internal Server Error with the exception message


    print("Order Response:", order_response)
if __name__ == '__main__':
    app.run(debug=True)