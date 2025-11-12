from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet สำหรับจัดการรีวิว (CRUD)
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # ให้เห็นทุกรีวิว หรือจะกรองเฉพาะของ user ก็ได้ เช่น:
        # return Review.objects.filter(customer=self.request.user)
        return Review.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        # ผูก customer เป็น user ปัจจุบัน
        serializer.save(customer=self.request.user)
