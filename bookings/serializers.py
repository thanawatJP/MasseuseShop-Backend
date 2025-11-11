from rest_framework import serializers
from .models import Appointment
from services.models import Service
from accounts.models import CustomUser

class AppointmentSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name", read_only=True)
    masseuse_name = serializers.CharField(source="masseuse.username", read_only=True)
    customer_name = serializers.CharField(source="customer.username", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "service", "service_name",
            "customer", "customer_name",
            "masseuse", "masseuse_name",
            "time_start", "time_end",
            "status", "payment_method",
        ]
        read_only_fields = ["customer"]
