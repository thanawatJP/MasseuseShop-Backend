# dashboard/views.py
from datetime import timedelta
from decimal import Decimal

from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser

from django.db.models import (
    Count, Sum, Avg, F, Value, DecimalField
)
from django.db.models.functions import TruncDate, Coalesce

from bookings.models import Appointment

CACHE_TTL_SUMMARY = 120
CACHE_TTL_TODAY   = 30
MAX_DAYS = 31

# ---------- helpers ----------
# 0 แบบ Decimal ให้ชนิดตรงกับ price_per_hour (DecimalField)
DEC_FIELD = DecimalField(max_digits=12, decimal_places=2)
ZERO_DEC  = Value(Decimal("0"), output_field=DEC_FIELD)

def _get_date_range(request):
    """
    คืนค่า (start_date, end_date) แบบ date โดยรวม end_date ด้วย
    และจำกัดช่วงสูงสุดไม่เกิน MAX_DAYS
    """
    try:
        days = int(request.GET.get("days", "7"))
    except (TypeError, ValueError):
        days = 7
    days = max(1, min(days, MAX_DAYS))

    end_date = timezone.localdate()              # วันนี้
    start_date = end_date - timedelta(days=days - 1)  # รวมวันนี้ => days วัน
    return start_date, end_date


# ---------- Views ----------
@method_decorator(cache_page(CACHE_TTL_SUMMARY), name="get")
class SummaryView(APIView):
    # permission_classes = [AllowAny]  # ชั่วคราวสำหรับทดสอบ
    permission_classes = [IsAdminUser]  # ชั่วคราวสำหรับทดสอบ

    def get(self, request):
        start_date, end_date = _get_date_range(request)
        base = Appointment.objects.filter(
            time_start__date__range=(start_date, end_date)
        )

        paid = base.filter(status="paid")

        revenue_total   = paid.aggregate(v=Coalesce(Sum("service__price_per_hour"), ZERO_DEC))["v"] or Decimal("0")
        bookings_total  = base.count()
        avg_per_booking = paid.aggregate(v=Coalesce(Avg("service__price_per_hour"), ZERO_DEC))["v"] or Decimal("0")

        by_status = list(
            base.values("status").annotate(count=Count("id")).order_by("status")
        )

        return Response({
            "range": {"from": start_date.isoformat(), "to": end_date.isoformat()},
            "kpis": {
                "revenue_total": float(revenue_total),
                "bookings_total": bookings_total,
                "avg_per_booking": float(avg_per_booking),
            },
            "by_status": by_status,
        })


@method_decorator(cache_page(CACHE_TTL_SUMMARY), name="get")
class RevenueSeriesView(APIView):
    # permission_classes = [AllowAny]  # ชั่วคราวสำหรับทดสอบ
    permission_classes = [IsAdminUser]  # ชั่วคราวสำหรับทดสอบ

    def get(self, request):
        start_date, end_date = _get_date_range(request)

        # รวมเฉพาะที่จ่ายแล้ว
        qs = (
            Appointment.objects
            .filter(status="paid", time_start__date__range=(start_date, end_date))
            .annotate(d=TruncDate("time_start"))
            .values("d")
            .annotate(
                revenue=Coalesce(Sum("service__price_per_hour"), ZERO_DEC),
                count=Count("id"),
            )
        )

        # map เป็น {date: record}
        got = {r["d"]: r for r in qs}

        # เติมทุกวันในช่วงให้ครบ (วันที่ไม่มีข้อมูลให้เป็น 0)
        series = []
        cur = start_date
        while cur <= end_date:
            r = got.get(cur)
            series.append({
                "date": cur.isoformat(),
                "revenue": float((r or {}).get("revenue", Decimal("0")) or 0),
                "count": int((r or {}).get("count", 0) or 0),
            })
            cur += timedelta(days=1)

        return Response({
            "range": {"from": start_date.isoformat(), "to": end_date.isoformat()},
            "series": series,
        })


@method_decorator(cache_page(CACHE_TTL_TODAY), name="get")
class TodayAppointmentsView(APIView):
    # permission_classes = [AllowAny]
    permission_classes = [IsAdminUser]  # ชั่วคราวสำหรับทดสอบ

    def get(self, request):
        today = timezone.localdate()

        qs = (
            Appointment.objects
            .select_related("service", "customer")
            .filter(time_start__date=today)
            .order_by("time_start")
            .annotate(price=F("service__price_per_hour"))
            .values("id", "time_start", "status",
                    "customer__username", "service__name", "price")
        )

        items = [{
            "id": r["id"],
            "time": r["time_start"].strftime("%H:%M"),
            "customer": r["customer__username"],
            "service": r["service__name"],
            "price": float(r["price"] or 0),
            "status": r["status"],
        } for r in qs]

        return Response({"date": today.isoformat(), "items": items})
