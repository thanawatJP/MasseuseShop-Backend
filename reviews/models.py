from django.db import models
from django.conf import settings

# Create your models here.
class Review(models.Model):
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_reviews"
    )
    rating = models.PositiveSmallIntegerField(default=5)  # 1-5 ดาว
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # เรียงจากใหม่ไปเก่า

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.rating}⭐)"