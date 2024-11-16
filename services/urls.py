from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import CategoryListCreateView, CategoryDetailView, ServiceListCreateView, ServiceDetailView, ReviewListCreateView, ReviewListByServiceView,FeaturedServiceListView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('', ServiceListCreateView.as_view(), name='services'),
    path('<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    path('featured/', FeaturedServiceListView.as_view(), name='service-detail'),
    path('reviews/create/', ReviewListCreateView.as_view(), name='review'),  
    path('reviews/<int:pk>/', ReviewListByServiceView.as_view(), name='review-detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
