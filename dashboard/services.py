from django.db.models import Sum, Count
from django.utils import timezone
from bookings.models import Appointment
from .models import AppointmentDaily

def recompute_day(day):
    qs_all  = Appointment.objects.filter(time_start__date=day)
    qs_paid = qs_all.filter(status='paid')
    agg = qs_paid.aggregate(rev=Sum('service__price'), cnt=Count('id'))
    AppointmentDaily.objects.update_or_create(
        day=day,
        defaults={
            "revenue": agg['rev'] or 0,
            "count_paid": agg['cnt'] or 0,
            "count_all": qs_all.count(),
        }
    )
