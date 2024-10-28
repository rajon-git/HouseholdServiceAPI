from rest_framework import generics
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from services.models import Service

class CartDetailView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

class AddToCartView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        service_id = request.data.get('service_id')
        quantity = request.data.get('quantity')

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({"detail": "Service not found."}, status=status.HTTP_404_NOT_FOUND)

        cart, created = Cart.objects.get_or_create(user=request.user)

        if quantity is None:
            quantity = 1
        else:
            quantity = int(quantity)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, service=service, defaults={'quantity': quantity})

        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return Response({'status': 'Item added to cart'}, status=status.HTTP_201_CREATED)

class CartItemListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cart_items=  CartItem.objects.filter(cart__user=self.request.user).select_related('service')
       
        return cart_items

class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.delete()
        return Response({"detail": "Cart item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class CartItemIncreaseQuantityView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.quantity += 1  
        cart_item.save()
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

class CartItemDecreaseQuantityView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.quantity > 1:
            cart_item.quantity -= 1 
            cart_item.save()
            serializer = self.get_serializer(cart_item)
            return Response(serializer.data)
        else:
            return Response({"detail": "Quantity cannot be less than 1."}, status=status.HTTP_400_BAD_REQUEST)
