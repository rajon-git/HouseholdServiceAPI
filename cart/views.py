from rest_framework import generics
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from services.models import Service
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

class ViewCartView(APIView):
    def get(self, request):
        session_key = request.GET.get("session_key") or request.session.session_key

        if not session_key:
            return Response({"detail": "Your cart is empty."}, status=status.HTTP_200_OK)
      
        if request.user.is_authenticated:
            user = request.user
            try:
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                return Response({"detail": "Cart not found for authenticated user."}, status=status.HTTP_404_NOT_FOUND)
        else:
            
            user = None
            try:
                cart = Cart.objects.get(session_key=session_key, user__isnull=True)
            except Cart.DoesNotExist:
                return Response({"detail": "Your cart is empty."}, status=status.HTTP_200_OK)

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key

        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

        cart.is_active = True
        cart.save()  

        service_id = request.data.get('service_id')
        quantity = request.data.get('quantity', 1)
        if not service_id or quantity < 1:
            return Response({"error": "Invalid service or quantity."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({"error": "Service not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            service=service,
            defaults={'quantity': quantity, 'is_active': True}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response({
            "message": "Item added to cart.",
            "cart_item": {
                "service_id": service.id,
                "quantity": cart_item.quantity,
            },
            "session_key": session_key,
        }, status=status.HTTP_201_CREATED)


class RemoveFromCartView(APIView):
    def delete(self, request, item_id):
        session_key = request.session.session_key
        cart = get_object_or_404(
            Cart,
            session_key=session_key if not request.user.is_authenticated else None,
            user=request.user if request.user.is_authenticated else None
        )

        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()  

        return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)

class ClearCartView(APIView):
    def delete(self, request):
        session_key = request.session.session_key
        cart = get_object_or_404(
            Cart,
            user=request.user if request.user.is_authenticated else None,
            session_key=session_key if not request.user.is_authenticated else None,
        )
        
        cart.items.all().delete()  
        return Response({"message": "Cart cleared successfully"}, status=status.HTTP_200_OK)
