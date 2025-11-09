from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Service
from .serializers import ServiceSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return []  # AllowAny
        return [IsAdminUser()]