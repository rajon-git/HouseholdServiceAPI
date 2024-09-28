from rest_framework import viewsets
from .models import Order
from .serializers import OrderSerializer
from cart.models import Cart  

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        user = serializer.validated_data.get('user')  
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            print("Cart does not exist for this user.")
            return 
        total_cost = sum(item.service.service_fee * item.quantity for item in cart.service.all())
      
        order = serializer.save(total_cost=total_cost)
        cart.delete() 
