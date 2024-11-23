from rest_framework import generics
from .models import Category, Service, Review
from .serializers import CategorySerializer, ServiceSerializer, ReviewSerializer,RelatedServiceSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
        
class ServiceListCreateView(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['category__slug'] 
    search_fields = ['title']
    ordering_fields = ['service_fee', 'is_available']
    ordering = ['service_fee']

    pagination_class = CustomPagination

class FeaturedServiceListView(generics.ListAPIView):
    queryset = Service.objects.filter(is_featured=True)
    serializer_class = ServiceSerializer 

class ServiceDetailView(generics.RetrieveAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
            return Response({"error": "Service not found"}, status=404)


class ReviewListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewListByServiceView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        service_id = self.kwargs['pk']
        return Review.objects.filter(service_id=service_id)
    
class DiscountedServiceList(generics.ListAPIView):
    queryset = Service.objects.filter(is_discount=True)
    serializer_class = ServiceSerializer

class RelatedServiceList(generics.ListAPIView):
    def get(self, request, service_id, format=None):
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            return Response({'error': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        related_services = Service.objects.filter(
            category=service.category
        ).exclude(id=service.id)  
        serializer = RelatedServiceSerializer(related_services, many=True)
        return Response(serializer.data)