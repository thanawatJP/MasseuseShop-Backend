from django.urls import path
from .views import SummaryView, RevenueSeriesView, TodayAppointmentsView

urlpatterns = [
    path("summary/", SummaryView.as_view()),
    path("revenue-series/", RevenueSeriesView.as_view()),
    path("today-appointments/", TodayAppointmentsView.as_view()),
]
