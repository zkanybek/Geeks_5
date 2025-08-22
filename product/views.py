from collections import OrderedDict
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.permissions import OR


from .models import Category, Product, Review
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer,
    ProductWithReviewsSerializer,
    CategoryValidateSerializer,
    ProductValidateSerializer,
    ReviewValidateSerializer
)
from common.permissions import IsOwner, IsAnonymous, IsModerator
from django.core.cache import cache
PAGE_SIZE = 5


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def get_page_size(self, request):
        return PAGE_SIZE


class CategoryListCreateAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CustomPagination

    def post(self, request, *args, **kwargs):
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = Category.objects.create(**serializer.validated_data)
        return Response(data=CategorySerializer(category).data,
                        status=status.HTTP_201_CREATED)


class CategoryDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.name = serializer.validated_data.get('name')
        instance.save()

        return Response(data=CategorySerializer(instance).data)


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination
    permission_classes = [IsOwner | IsAnonymous | IsModerator]

    def post(self, request, *args, **kwargs):
        email = request.auth.get('email')
        print(f"email: {email}")
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get validated data
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category = serializer.validated_data.get('category')

        # Create product
        product = Product.objects.create(
            title=title,
            description=description,
            price=price,
            category=category,
            owner=request.user,
        )

        return Response(data=ProductSerializer(product).data,
                        status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        cached_data = cache.get("product_list")
        if cached_data:
            print("работает редис!")
            return Response(data=cached_data, status=status.HTTP_200_OK)
        response = super().get(request, *args, **kwargs)
        print("обычный response")
        if response.data.get("total", 0) > 0:
            cache.set("product_list", response.data, timeout=120)
        return response

class ProductDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    permission_classes = [IsOwner | IsAnonymous | IsModerator ]

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category = serializer.validated_data.get('category')
        product.save()

        return Response(data=ProductSerializer(product).data)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get validated data
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product = serializer.validated_data.get('product')

        # Create review
        review = Review.objects.create(
            text=text,
            stars=stars,
            product=product
        )

        return Response(data=ReviewSerializer(review).data,
                        status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        review = self.get_object()
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product = serializer.validated_data.get('product')
        review.save()

        return Response(data=ReviewSerializer(review).data)


class ProductWithReviewsAPIView(APIView):
    def get(self, request):
        paginator = CustomPagination()
        products = Product.objects.select_related('category').prefetch_related('reviews').all()
        result_page = paginator.paginate_queryset(products, request)

        serializer = ProductWithReviewsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    

class OwnerProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user).select_related('category')