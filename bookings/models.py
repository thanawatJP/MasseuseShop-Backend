from django.db import models
from django.conf import settings
from services.models import Service

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD = [
        ('credit_card', 'Credit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
    ]

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="appointments")
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_appointments"
    )
    masseuse = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="masseuse_appointments"
    )
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, default='cash')

    def __str__(self):
        return f"{self.customer.username} - {self.service.name} ({self.status})"
