import requests
from datetime import datetime
import base64


CONSUMER_KEY = "kvYg2X2Rc5gmS1vjLo3wNBWoAGrkfqs7fw8CGJbEl3pJLlGo"
CONSUMER_SECRET = "mqNdGZEE7RYdeWxZmgKGQMH3ghWOTe9BfmdjcrjQZMQnOHlQGJqH9fpGJEnqC73g"
BUSINESS_SHORTCODE = "174379"
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
CALLBACK_URL = "https://yourdomain.com/callback"

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    return response.json()["access_token"]

def generate_password():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    data_to_encode = BUSINESS_SHORTCODE + PASSKEY + timestamp
    encoded_string = base64.b64encode(data_to_encode.encode()).decode("utf-8")
    return encoded_string, timestamp

def stk_push(phone: str, amount: float):
    access_token = get_access_token()
    password, timestamp = generate_password()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "Service Payment",
        "TransactionDesc": "Payment for Service"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


