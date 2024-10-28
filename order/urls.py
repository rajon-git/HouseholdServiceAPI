from django.urls import path
from .views import OrderCreateView, UserOrderListView, OrderDetailView

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('/', UserOrderListView.as_view(), name='user-orders'),
     path('<int:pk>/', OrderDetailView.as_view(), name='order-detail')
]
