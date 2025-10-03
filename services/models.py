from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)  # เช่น "นวดแผนไทย"
    description = models.TextField(blank=True, null=True)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="services/", blank=True, null=True)  # 👈 เพิ่มรูปภาพ

    def __str__(self):
        return f"{self.name} - {self.price_per_hour} THB/hr"
