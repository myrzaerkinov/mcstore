from rest_framework import serializers
from products.models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "id name".split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "id text stars author".split()


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Product
        fields = "title image description cost category reviews rating".split()

    def get_category(self, product):
        return product.category.name
