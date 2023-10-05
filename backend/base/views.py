from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer
# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/products/create/',

        '/api/products/upload/',

        '/api/products/<id>/reviews/',

        '/api/products/top/',
        '/api/products/<id>/',

        '/api/products/delete/<id>/',
        '/api/products/update/<id>/',
    ]
    return Response(routes)

@api_view(['GET'])
def getProducts(request):
    products = ProductSerializer(Product.objects.all(), many=True)
    return Response(products.data)

@api_view(['GET'])
def getProductById(request, pk):
    try:
        product = Product.objects.get(_id = pk)
    except Product.DoesNotExist:
        return Response(status= 404)
    
    return Response(ProductSerializer(product, many=False).data)
