from django.urls import path
from .views import CookieTokenObtainPairView, LogoutView, MeView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("me/", MeView.as_view(), name="get_me"),
    path("login/", CookieTokenObtainPairView.as_view(), name="cookie_token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]