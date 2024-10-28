from django.core.mail import send_mail
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.save()
        
        send_mail(
            'Order Confirmation',
            f'Thank you for your order! Your order ID is {order.id}.',
            settings.DEFAULT_FROM_EMAIL,
            [order.user.email],
            fail_silently=False,
        )

        send_mail(
            'New Order Received',
            f'A new order has been placed by {order.user.username}. Order ID: {order.id}.',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],  
            fail_silently=False,
        )

class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        order = super().get_object()
        if order.user != self.request.user:
            raise PermissionDenied("You do not have permission to view this order.")
        return order
