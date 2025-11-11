from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Appointment
from .serializers import AppointmentSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        สร้างการจองโดยผูก customer เป็น user ที่ล็อกอินอยู่
        """
        serializer.save(customer=self.request.user, status="pending")

    def get_queryset(self):
        """
        ถ้าเป็น staff ให้ดูทั้งหมด
        ถ้าเป็นลูกค้า ให้เห็นเฉพาะของตัวเอง
        """
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all().order_by("-time_start")
        return Appointment.objects.filter(customer=user).order_by("-time_start")
    
    @action(detail=True, methods=["patch"], url_path="mark-paid")
    def mark_paid(self, request, pk=None):
        """
        ใช้สำหรับอัปเดตสถานะนัดหมายเป็น paid หลังจ่ายสำเร็จ
        """
        try:
            appointment = self.get_object()
            appointment.status = "paid"
            appointment.save()
            return Response({"message": "Appointment marked as paid"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

