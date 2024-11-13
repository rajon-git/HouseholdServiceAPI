from rest_framework import serializers
from .models import Order, OrderItem
from cart.models import CartItem, Service

class OrderItemSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())

    class Meta:
        model = OrderItem
        fields = ['service', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['user', 'cart', 'items', 'total_price', 'status']
        read_only_fields = ['total_price', 'status']

   
