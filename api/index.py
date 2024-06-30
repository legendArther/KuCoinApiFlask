from flask import Flask, jsonify, request
from dotenv import load_dotenv
from neo_api_client import NeoAPI
  
# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)

#print('login')

no = "+918839000041"
pas = "Happy123$$"
ck = "N7RD0Ydol8qBNE22SMffcT3FXpMa"
cs = "OfE3Hxw4QBAj7jSbrYsM5V01EQYa"

client = NeoAPI(consumer_key=ck, consumer_secret=cs, environment='prod',
                access_token=None, neo_fin_key=None)
client.login(mobilenumber=no, password=pas)

@app.route('/')
def home():
    quantity = test()
    return (quantity)

@app.route('/login')
def login():
    res = client.login(mobilenumber=no, password=pas)
    return(res)

@app.route('/otp', methods=['GET'])
def otp():
    try:
        myotp = request.args.get('myotp')
        client.session_2fa(OTP=str(myotp))
     #   get_max_quantity() #comment
        return client.scrip_master()
    except Exception as e:
        print("Exception : %s\n" % e)
        return str(e)
    
@app.route('/buy', methods=['GET', 'POST'])
def buy():
    symbol = request.args.get('symbol')
    try:
        if symbol == 'buy':
            order_response = order('B')
            # Check the status of the order response
            if order_response['stat'] != 'Ok':
                return jsonify(order_response), 400  # Returning a 400 Bad Request with the error details

            return jsonify({'message': 'Order placed successfully'}), 200
        
        elif symbol == 'sell':
            order_response = order('S')
            if order_response['stat'] != 'Ok':
                return jsonify(order_response), 400  # Returning a 400 Bad Request with the error details

            return jsonify({'message': 'Order placed successfully'}), 200
    except Exception as e:
        error_message = f"Exception on /buy: {str(e)}"
        print(error_message)
        return jsonify({'error': error_message}), 500  # Returning a 500 Internal Server Error with the exception message

def order(symb):
    max_quantity = get_max_quantity()
    try:
        order_response = client.place_order(
            exchange_segment='nse_cm',
            product='MIS',
            price='',
            order_type='MKT',
            quantity=str(max_quantity),
            validity='DAY',
            trading_symbol='TATASTEEL-EQ',
            transaction_type=symb
        )
        return order_response
    except Exception as e:
        error_message = f"Exception when placing order: {str(e)}"
        print(error_message)
        return {'stat': 'Error', 'message': error_message}
    
    
def get_max_quantity():
    try:
        margin_data = client.margin_required(
            exchange_segment="nse_cm",  # Example segment
            price="0",  # Dummy price to get margin data
            order_type="MKT",
            product="MIS",
            quantity="1",  # Dummy quantity
            instrument_token="3499",  # Dummy instrument token, replace with a valid one
            transaction_type="B",
        )
        available_cash = float(margin_data['data']['avlCash'])
        margin = float(margin_data['data']['totMrgnUsd'])
        max_quantity = int(available_cash / margin)
        print(f"Available Cash: {available_cash}")
        print(f"Total Margin: {margin}")
        print(f"Maximum Quantity: {max_quantity}")
        return str(max_quantity)
    except Exception as e:
        return(f"Exception when fetching available cash: {e}")
def test():
    try:
        margin_data = client.margin_required(
            exchange_segment="nse_cm",  # Example segment
            price="0",  # Dummy price to get margin data
            order_type="MKT",
            product="MIS",
            quantity="1",  # Dummy quantity
            instrument_token="3499",  # Dummy instrument token, replace with a valid one
            transaction_type="B",
        )
        available_cash = float(margin_data['data']['avlCash'])
        margin = float(margin_data['data']['totMrgnUsd'])
        max_quantity = int(available_cash / margin)
        print(f"Available Cash: {available_cash}")
        print(f"Total Margin: {margin}")
        print(f"Maximum Quantity: {max_quantity}")
        return str(max_quantity)
    except Exception as e:
        return(f"Exception when fetching available cash: {e}")

if __name__ == '__main__':
    app.run(debug=True)