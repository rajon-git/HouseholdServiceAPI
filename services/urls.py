from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('all', views.ServiceListViewSet)

urlpatterns = [
    path('<int:id>/', views.ServiceDetailView.as_view(), name='service-detail'),
    path('', include(router.urls)),
]
