
from django.urls import path
from base.views import payment_views as views

urlpatterns = [
    path('create_order/<str:orderId>', views.createOrder, name='create-order'),
    path('capture_order/<str:orderId>', views.captureOrder, name='capture-order'),
]
