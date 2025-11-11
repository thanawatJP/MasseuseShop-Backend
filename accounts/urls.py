from django.urls import path
from .views import CookieTokenObtainPairView, CookieTokenRefreshView,LogoutView, MeView, RegisterView, AddStaffView, ProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("me/", MeView.as_view(), name="get_me"),
    path("login/", CookieTokenObtainPairView.as_view(), name="cookie_token_obtain_pair"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("add-staff/", AddStaffView.as_view(), name="add-staff"),
]