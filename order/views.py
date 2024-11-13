from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart, CartItem, Service
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, permissions
from .serializers import OrderSerializer


class OrderCreateView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."},
                             status=status.HTTP_401_UNAUTHORIZED)

        cart = Cart.objects.filter(
            user=request.user,
            is_active=True,
            items__is_active=True  
        ).first()

        if not cart:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        order_items_data = request.data.get('items', [])
        if not order_items_data:
            return Response({"detail": "No items provided."}, status=status.HTTP_400_BAD_REQUEST)

        total_price = 0

        order = Order.objects.create(user=request.user, cart=cart)

        for item_data in order_items_data:
            try:
                service = Service.objects.get(id=item_data['service'])
            except Service.DoesNotExist:
                return Response({"detail": "Service not found."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                cart_item = CartItem.objects.get(cart=cart, service=service)
            except CartItem.DoesNotExist:
                return Response({"detail": "Cart item not found for the selected service."}, status=status.HTTP_400_BAD_REQUEST)

            total_price += cart_item.get_total_price()

            OrderItem.objects.create(order=order, service=cart_item.service, quantity=item_data['quantity'])

        order.total_price = total_price
        order.save()
        cart.items.all().delete()
        cart.is_active = False  
        cart.save()

        # **Delete the cart** after the order has been processed
        # cart.delete()
        subject = f"Order Confirmation - Order #{order.id}"
        message = f"Dear {request.user.username},\n\nYour order has been successfully placed!\nOrder ID: {order.id}\nTotal Price: ${order.total_price}\n\nThank you for shopping with us!"
        admin_message = f"A new order has been placed.\nOrder ID: {order.id}\nCustomer: {request.user.username}\nTotal Price: ${order.total_price}"

        try:
            # Send email to the user
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )

            send_mail(
                f"New Order Notification - Order #{order.id}",
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  
                fail_silently=False,
            )

        except Exception as e:
            return Response({"detail": f"Error sending email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    
class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
