from django.urls import path
from .views import CartDetailView, AddToCartView, CartItemListView, CartItemIncreaseQuantityView, CartItemDecreaseQuantityView, CartItemDeleteView

urlpatterns = [
    path('<int:pk>/', CartDetailView.as_view(), name='cart-detail'),  
    path('', CartItemListView.as_view(), name='cart-list'),  
    path('add/', AddToCartView.as_view(), name='cart-create'), 
    path('increase/<int:pk>/', CartItemIncreaseQuantityView.as_view(), name='cart-increase'), 
    path('decrease/<int:pk>/', CartItemDecreaseQuantityView.as_view(), name='cart-decrease'),  
    path('delete/<int:pk>/', CartItemDeleteView.as_view(), name='cart-delete'),  
]
