from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VenueViewSet, SeatViewSet, BookingViewSet


router = DefaultRouter()
router.register(r"venues", VenueViewSet)
router.register(r"seats", SeatViewSet)
router.register(r"bookings", BookingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
