from django.urls import path
from .views import (
    CategoryListCreateView,
    CategoryDetailUpdateDeleteView,
    ProductListCreateView,
    ProductDetailUpdateDeleteView,
    ReviewListCreateView,
    ReviewDetailUpdateDeleteView,
    ProductReviewsView,
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailUpdateDeleteView.as_view(), name='category-detail-update-delete'),

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailUpdateDeleteView.as_view(), name='product-detail-update-delete'),

    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailUpdateDeleteView.as_view(), name='review-detail-update-delete'),

    path('products/reviews/', ProductReviewsView.as_view(), name='product-reviews'),
]
