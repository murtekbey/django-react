from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderSerializer

from datetime import datetime

import requests
import json
from backend.settings import PAYPAL_ID, PAYPAL_BASE_URL, PAYPAL_SECRET

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





@api_view(['GET'])
def createOrder(request, orderId):
    order = Order.objects.get(_id=orderId)
    payload = {
        'intent': "CAPTURE",
        'purchase_units': [
            {"amount": {"currency_code": "USD", "value": str(order.totalPrice)}}]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + getAccessToken()
    }

    order_response = requests.post(
        order_url, data=json.dumps(payload), headers=headers)

    print(order_response.text)
    print(order_response)
    if order_response.status_code != 201:
        return False, 'Failed to create PayPal payment.', None

    return Response(order_response.json(), status=status.HTTP_200_OK)

@api_view(['GET'])
def captureOrder(request, orderId):
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + getAccessToken()
    }

    order_response = requests.post(
        order_url + '/' + orderId + '/capture', headers=headers)

    print(order_response)
    if order_response.status_code != 201:
        return Response({"detail": "Failed to create order"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    return Response(order_response.json(), status=status.HTTP_200_OK)


def getAccessToken():
    token_response = requests.post(token_url, auth=(
        client_id, secret), data=token_payload, headers=token_headers)

    return token_response.json()['access_token']