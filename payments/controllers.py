# payment/controllers.py
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bookings.models import Appointment

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreatePaymentIntentView(APIView):
    """สร้าง PaymentIntent จากข้อมูลนัดหมายจริง"""

    def post(self, request):
        appointment_id = request.data.get("appointment_id")

        if not appointment_id:
            return Response({"error": "appointment_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            appointment = Appointment.objects.select_related("service").get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)

        # ดึงราคาจาก Service (บาท เป็น สตางค์ เพราะ Stripe ใช้สตางค์)
        try:
            amount = int(appointment.service.price_per_hour * 100)
        except Exception as e:
            return Response({"error": f"Invalid service price: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="thb",
                automatic_payment_methods={"enabled": True},
                metadata={"appointment_id": appointment_id},
            )
            return Response(
                {
                    "client_secret": intent.client_secret,
                    "publishable_key": settings.STRIPE_PUBLISHABLE_KEY,
                    "amount": amount,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class StripeWebhookView(APIView):
    """รับ Webhook จาก Stripe ใช้ตรวจสถานะการชำระ"""

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if event["type"] == "payment_intent.succeeded":
            payment_intent = event["data"]["object"]
            appointment_id = payment_intent["metadata"].get("appointment_id")

            if appointment_id:
                Appointment.objects.filter(id=appointment_id).update(status="paid")

        return Response(status=status.HTTP_200_OK)
