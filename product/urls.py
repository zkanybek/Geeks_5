# product/urls.py

from django.urls import path
from .views import (
    category_list,
    category_detail,
    product_list,
    product_detail,
    review_list,
    review_detail,
    CategoryListAPIView,
    ProductReviewListAPIView,
)


urlpatterns = [
    path('categories/', category_list, name='category-list'),
    path('categories/<int:pk>/', category_detail, name='category-detail'),
    path('api/v1/categories/', CategoryListAPIView.as_view()),

    path('products/', product_list, name='product-list'),
    path('products/<int:pk>/', product_detail, name='product-detail'),

    path('reviews/', review_list, name='review-list'),
    path('reviews/<int:pk>/', review_detail, name='review-detail'),
    path('products/reviews/', ProductReviewListAPIView.as_view(), name='product-reviews'),
]
