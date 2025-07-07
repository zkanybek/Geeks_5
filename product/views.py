from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .seriallzers import CategorySerializer, ProductSerializer, ReviewSerializer
from .models import Category, Product, Review


# @api_view(http_method_names=['GET'])
# def product_list_api_view(request):
#     return Response(
#         data={'text': 'hello world'},
#         status=status.HTTP_200_OK
#     )

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetail(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
# Create your views here.
