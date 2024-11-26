# NeoAPI Trading Bot

This is a Flask-based Python application that interacts with the **Neo API** to manage trading activities on the **NSE (National Stock Exchange)**. The app provides RESTful endpoints for login, OTP verification, checking margins, placing buy/sell orders, and fetching position details. It's designed for users who want to automate trading workflows.

---

## Features

1. **User Authentication**  
   - Login via mobile number and password.  
   - Supports OTP-based 2FA for secure access.

2. **Trade Execution**  
   - Place market orders (`BUY`/`SELL`) with dynamic quantity adjustment based on positions and available cash.  
   - Supports intraday (`MIS`) trades.

3. **Margin Calculation**  
   - Calculate the maximum quantity for trades based on available cash and margin requirements.

4. **Position Tracking**  
   - Fetch current position details and calculate total net quantities for optimized trading.

5. **API Testing**  
   - Endpoint for testing order placement and margin calculations.

6. **Error Handling**  
   - Provides detailed error messages for API issues or invalid inputs.

---

## Endpoints

1. `/`  
   - Returns the maximum quantity available for trading.  
   - **Method:** GET  

2. `/login`  
   - Authenticates the user with their credentials.  
   - **Method:** GET  

3. `/otp`  
   - Verifies the OTP for completing the login process.  
   - **Method:** GET  
   - **Parameters:**  
     - `myotp`: The OTP received on the registered mobile number.  

4. `/buytest`  
   - Returns a combined JSON response of URL parameters and POST data for testing.  
   - **Methods:** GET, POST  

5. `/buy`  
   - Executes a buy or sell order.  
   - **Methods:** GET, POST  
   - **JSON Body:**  
     - `symbol`: `"buy"` or `"sell"`.  

---

## Setup

1. Clone the repository:  
   ```bash
   git clone <repository_url>
   cd neoapi-trading-bot
   ```

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in a `.env` file:  
   ```dotenv
   CONSUMER_KEY=your_consumer_key
   CONSUMER_SECRET=your_consumer_secret
   MOBILE_NUMBER=your_mobile_number
   PASSWORD=your_password
   ```

4. Run the app:  
   ```bash
   python app.py
   ```

5. Access the app at `http://127.0.0.1:5000`.

---

## Dependencies

- Flask
- Neo API Client
- Python Dotenv

---

## Notes

- Replace the dummy instrument token (`3499`) with a valid token for accurate trading operations.
- The application is configured for the **production** environment (`prod`).
- Ensure your Neo API credentials have sufficient permissions for trading.

---

## License

This project is licensed under the [MIT License](LICENSE).
