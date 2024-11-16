from django.urls import path
from .views import ViewCartView, AddToCartView, ClearCartView, RemoveFromCartView,IncrementCartItemQuantityView,DecrementCartItemQuantityView


urlpatterns = [
    path('', ViewCartView.as_view(), name='cart-list'),  
    path('add/', AddToCartView.as_view(), name='cart-create'), 
    path('remove/<int:item_id>/', RemoveFromCartView.as_view(), name='cart-delete'),  
    path('clear_cart/', ClearCartView.as_view(), name='cart-delete'),  
    path('<int:item_id>/increment/', IncrementCartItemQuantityView.as_view(), name='increment_cart_item'),
    path('<int:item_id>/decrement/', DecrementCartItemQuantityView.as_view(), name='decrement_cart_item'),
]
