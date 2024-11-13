from rest_framework import generics
from .models import Category, Service, Review
from .serializers import CategorySerializer, ServiceSerializer, ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .pagination import CustomPagination


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
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetailView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer