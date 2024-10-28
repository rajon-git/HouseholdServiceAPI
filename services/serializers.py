from rest_framework import serializers
from .models import Category, Service, Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Service
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(read_only=True) 
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Review
        fields = "__all__"
