from rest_framework import serializers
from .models import Category, Service, Review
from authapp.serializers import UserSerializer

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

    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["user"]
