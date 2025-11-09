from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path("me/", MeView.as_view(), name="get_me"),
    path("login/", CookieTokenObtainPairView.as_view(), name="cookie_token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="register"),
    path("add-staff/", AddStaffView.as_view(), name="add-staff"),
    path("", include(router.urls)),
]