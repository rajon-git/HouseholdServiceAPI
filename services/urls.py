from django.urls import path
from .views import CategoryListCreateView, CategoryDetailView, ServiceListCreateView, ServiceDetailView, ReviewListCreateView, ReviewDetailView,FeaturedServiceListView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('', ServiceListCreateView.as_view(), name='services'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('featured/', FeaturedServiceListView.as_view(), name='service-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review'),  
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
