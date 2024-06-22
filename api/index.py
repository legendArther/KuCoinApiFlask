from flask import Flask, jsonify, request, g
from dotenv import load_dotenv
import os
from neo_api_client import NeoAPI

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['NEOAPI_CONSUMER_KEY'] = os.getenv('NEOAPI_CONSUMER_KEY')
    app.config['NEOAPI_CONSUMER_SECRET'] = os.getenv('NEOAPI_CONSUMER_SECRET')
    app.config['NEOAPI_MOBILE_NUMBER'] = os.getenv('NEOAPI_MOBILE_NUMBER')
    app.config['NEOAPI_PASSWORD'] = os.getenv('NEOAPI_PASSWORD')
    app.config['NEOAPI_ENVIRONMENT'] = 'prod'

    # Create and login NeoAPI client on app initialization
    neoapi_client = NeoAPI(
        consumer_key=app.config['NEOAPI_CONSUMER_KEY'],
        consumer_secret=app.config['NEOAPI_CONSUMER_SECRET'],
        environment=app.config['NEOAPI_ENVIRONMENT'],
        access_token=None,
        neo_fin_key=None
    )
    
    # Perform login
    try:
        neoapi_client.login(
            mobilenumber=app.config['NEOAPI_MOBILE_NUMBER'],
            password=app.config['NEOAPI_PASSWORD']
        )
        print("NeoAPI login successful")
    except Exception as e:
        print(f"NeoAPI login failed: {str(e)}")
        # You might want to raise an exception here if login is critical

    def get_neoapi_client():
        if 'neoapi_client' not in g:
            g.neoapi_client = neoapi_client
        return g.neoapi_client

    @app.teardown_appcontext
    def close_neoapi_client(e=None):
        client = g.pop('neoapi_client', None)
        if client is not None:
            # Close the client if necessary
            # client.close()  # Uncomment if NeoAPI has a close method
            pass

    # Make get_neoapi_client accessible to all app functions
    app.get_neoapi_client = get_neoapi_client

    @app.route('/')
    def home():
        return 'Hello, NeoAPI client is initialized and logged in'

    @app.route('/otp', methods=['POST'])
    def handle_otp():
        data = request.json
        otp = data.get('otp')
        if not otp:
            return jsonify({"error": "OTP is required"}), 400

        client = app.get_neoapi_client()
        try:
            client.session_2fa(OTP=otp)
            client.scrip_master()
            return jsonify({"message": "OTP verified and scrip master updated"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)