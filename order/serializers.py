from rest_framework import serializers
from .models import Order
from cart.models import CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'service', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cart.items', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'cart', 'total_amount', 'created_at', 'updated_at', 'items']
