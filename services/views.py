# views.py
from rest_framework import viewsets
from .models import Service
from .serializers import ServiceSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class ServiceListViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceDetailView(APIView):
    def get_object(self, id):
        try:
            return Service.objects.get(id=id)
        except Service.DoesNotExist:
            return None

    def get(self, request, id):
        service = self.get_object(id)
        if service is not None:
            serializer = ServiceSerializer(service)
            return Response(serializer.data)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
