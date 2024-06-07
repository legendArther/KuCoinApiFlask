import ccxt

api_key = '6662b0fbb2f56f0001658fcb'
api_secret = '5b3a97e7-538e-4cd5-aafe-991725ba9a23'
api_password = 'Qwerty123'

# Initialize the KuCoin futures exchange
exchange = ccxt.kucoinfutures({
    'apiKey': api_key,
    'secret': api_secret,
    'password': api_password,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'  # prefer "future", "margin" or "swap"
    }
})

try:
    # Load markets
    markets = exchange.load_markets()

    # Select the symbol for trading
    symbol = 'BTC/USDT:USDT'  # Example for BTC/USDT futures

    # Fetch balance
    balance = exchange.fetch_balance()
    print(balance)

    # Fetch the current order book
    order_book = exchange.fetch_order_book(symbol)
    print(order_book)
    
except ccxt.AuthenticationError as e:
    print(f"Authentication failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")