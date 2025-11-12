from rest_framework import serializers
from .models import Review
from accounts.models import CustomUser


class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.username", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "customer", "customer_name",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["customer", "created_at"]
    