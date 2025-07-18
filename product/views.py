from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView

from .models import Category, Product, Review
from .seriallzers import (
    CategorySerializer, 
    ProductSerializer, 
    ReviewSerializer, 
    ProductWithReviewsSerializer )

# Категории

@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = CategorySerializer(category)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['PUT', 'DELETE'])
def category_update_delete(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=204)

# Продукты

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

# --- Products ---

@api_view(['GET', 'POST'])
def product_list_create(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['PUT', 'DELETE'])
def product_update_delete(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=204)


@api_view(['GET'])
def review_list(request):
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def review_detail(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ReviewSerializer(review)
    return Response(serializer.data)

# --- Reviews ---

@api_view(['GET', 'POST'])
def review_list_create(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['PUT', 'DELETE'])
def review_update_delete(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        review.delete()
        return Response(status=204)


@api_view(['GET'])
def product_reviews_view(request):
    products = Product.objects.prefetch_related('reviews').all()
    serializer = ProductWithReviewsSerializer(products, many=True)
    return Response(serializer.data)

class ProductReviewListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductWithReviewsSerializer

class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

