from rest_framework import serializers
from .models import Service
from category.models import Category

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'image', 'description', 'category', 'service_fee', 'is_available']
