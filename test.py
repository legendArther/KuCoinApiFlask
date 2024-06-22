import requests

url = "https://ku-coin-api-flask.vercel.app/otp"
data = {
    "myotp": "1210"
}

response = requests.post(url, json=data)

print(response.json())
