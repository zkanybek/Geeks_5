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

    category_list_create,
    category_update_delete,
    product_list_create,
    product_update_delete,
    review_list_create,
    review_update_delete,
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

    path('categories/', category_list_create),
    path('categories/<int:id>/', category_update_delete),

    path('products/', product_list_create),
    path('products/<int:id>/', product_update_delete),

    path('reviews/', review_list_create),
    path('reviews/<int:id>/', review_update_delete),
]
