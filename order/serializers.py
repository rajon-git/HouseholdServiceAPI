from rest_framework import serializers
from .models import Order, OrderItem
from cart.models import CartItem, Service
from services.serializers import ServiceSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    # service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    service = ServiceSerializer()
    class Meta:
        model = OrderItem
        fields = "__all__"

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ['total_price', 'status','items']

    

   
