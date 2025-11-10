from django.db import models

class AppointmentDaily(models.Model):
    day = models.DateField(unique=True)
    revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    count_paid = models.IntegerField(default=0)
    count_all  = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)