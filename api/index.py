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


if __name__ == '__main__':
    app.run(debug=True)
