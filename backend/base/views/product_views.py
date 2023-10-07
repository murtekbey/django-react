from rest_framework.decorators import api_view
from rest_framework.response import Response

from base.serializers import ProductSerializer
from base.models import Product

@api_view(['GET'])
def getProducts(request):
    products = ProductSerializer(Product.objects.all(), many=True)
    return Response(products.data)


@api_view(['GET'])
def getProductById(request, pk):
    try:
        product = Product.objects.get(_id=pk)
    except Product.DoesNotExist:
        return Response(status=404)

    return Response(ProductSerializer(product, many=False).data)
