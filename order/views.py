from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, OrderItem
from cart.models import Cart, CartItem, Service
from .serializers import OrderSerializer

class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated] 

    def post(self, request):
        user = request.user
        name = request.data.get('name')
        phone = request.data.get('phone')
        house = request.data.get('house')
        road= request.data.get('road')
        ward= request.data.get('ward')
        city = request.data.get('city')
        state = request.data.get('state')
        payment_type = request.data.get('payment_type', 'cash')

        if not all([name, phone, house, road, ward, city, state]):
            return Response({"detail": "All address fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.filter(user=user, is_active=True, items__is_active=True).first()
        if not cart:
            return Response({"detail": "Active cart not found."}, status=status.HTTP_404_NOT_FOUND)

        order_items_data = request.data.get('items', [])
        if not order_items_data:
            return Response({"detail": "No items provided in the request."}, status=status.HTTP_400_BAD_REQUEST)

        total_price = 0
        order = Order.objects.create(user=user, cart=cart, payment_type=payment_type)  # Create the order instance

        for item_data in order_items_data:
            service_id = item_data.get('service')
            quantity = item_data.get('quantity')

            if not service_id or not quantity:
                return Response({"detail": "Service ID and quantity are required for all items."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                service = Service.objects.get(id=service_id)
                cart_item = CartItem.objects.get(cart=cart, service=service)
            except (Service.DoesNotExist, CartItem.DoesNotExist):
                return Response({"detail": f"Invalid service or cart item: {service_id}"}, status=status.HTTP_400_BAD_REQUEST)

            total_price += cart_item.get_total_price()
            OrderItem.objects.create(order=order, service=cart_item.service, quantity=quantity)

        order.total_price = total_price
        order.name = name
        order.phone = phone
        order.house = house
        order.road = road
        order.ward = ward
        order.city = city
        order.state = state
        order.save()

        cart.items.all().delete()
        cart.is_active = False
        cart.save()

        subject = f"Order Confirmation - Order #{order.id}"
        user_message = f"""
        Dear {user.username},

        Your order has been successfully placed!
        Order ID: {order.id}
        Total Price: ${order.total_price}

        Address Details:
        Contact Name: {name}
        Phone: {phone}
        Address: House #{house}, Road #{road}, Ward #{ward}, {city}, {state}

        Thank you for shopping with us!
        """
        admin_message = f"New order placed.\nOrder ID: {order.id}\nCustomer: {user.username}\nTotal Price: ${order.total_price}"

        try:
            send_mail(subject, user_message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
            send_mail(f"New Order Notification - Order #{order.id}", admin_message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL], fail_silently=False)
        except Exception as e:
            return Response({"detail": f"Email sending failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        try:
            order_id = kwargs.get('pk') 
            order = self.get_queryset().get(id=order_id)
            return Response(self.serializer_class(order).data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found or you don't have permission to view it."}, status=status.HTTP_404_NOT_FOUND)
