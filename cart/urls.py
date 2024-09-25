from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register the CartViewSet
router = DefaultRouter()
router.register('carts', views.CartViewSet)

urlpatterns = [
    path('', include(router.urls)), 
]
