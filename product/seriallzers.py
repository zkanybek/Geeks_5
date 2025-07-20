from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.validators import UniqueValidator
from django.core.validators import MinValueValidator, MaxValueValidator


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Category.objects.all())]
    )
    products_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=Product.objects.all())]
    )
    description = serializers.CharField(min_length=10)
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']


class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(min_length=5)
    stars = serializers.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'text', 'product', 'stars']


class ProductWithReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'average_rating', 'reviews']

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum(r.stars for r in reviews) / reviews.count(), 2)
        return None
