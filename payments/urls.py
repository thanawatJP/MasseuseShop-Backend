from django.urls import path
from .controllers import CreatePaymentIntentView, StripeWebhookView

urlpatterns = [
    path("create-intent/", CreatePaymentIntentView.as_view(), name="create-payment-intent"),
]
