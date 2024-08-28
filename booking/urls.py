from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookingViewSet, SeatViewSet, VenueViewSet

router = DefaultRouter()
router.register(r"venues", VenueViewSet)
router.register(r"seats", SeatViewSet)
router.register(r"bookings", BookingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
