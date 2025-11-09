from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'', AppointmentViewSet, basename='appointment')

urlpatterns = router.urls
