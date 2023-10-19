from backend.settings import PAYPAL_ID, PAYPAL_BASE_URL, PAYPAL_SECRET

import requests
import json

# Set up PayPal API credentials
client_id = PAYPAL_ID
secret = PAYPAL_SECRET
url = PAYPAL_BASE_URL

# Set up API endpoints
base_url = url
token_url = base_url + '/v1/oauth2/token'
order_url = base_url + '/v2/checkout/orders'

# Request an access token
token_payload = {'grant_type': 'client_credentials'}
token_headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}


def getAccessToken():
    token_response = requests.post(token_url, auth=(
        client_id, secret), data=token_payload, headers=token_headers)

    return token_response.json()['access_token']


def createPaypalOrder(currency, amount):
    payload = {
        'intent': "CAPTURE",
        'purchase_units': [
            {"amount": {"currency_code": currency, "value": amount}}]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + getAccessToken()
    }

    create_order_response = requests.post(
        order_url, data=json.dumps(payload), headers=headers)
    

    if create_order_response.status_code != 201:
        raise Exception("Create order has been failed")

    return create_order_response.json()


def capturePaypalOrder(orderId):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + getAccessToken()
    }

    capture_order_response = requests.post(
        order_url + '/' + orderId + '/capture', headers=headers)

    if capture_order_response.status_code != 200:
        raise Exception("Capture order has been failed")

    return capture_order_response.json()
