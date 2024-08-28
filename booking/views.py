from typing import Any, Dict

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Booking, Seat, Venue
from .serializers import BookingSerializer, SeatSerializer, VenueSerializer


class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(
        self, request: Request, *args: Any, **kwargs: Dict[str, Any]
    ) -> Response:
        # Check if the seat is already booked at the requested date and time
        seat_id: str = request.data.get("seat", "")
        booking_date: str = request.data.get("booking_date", "")
        booking_time: str = request.data.get("booking_time", "")

        if Booking.objects.filter(
            seat_id=seat_id, booking_date=booking_date, booking_time=booking_time
        ).exists():
            return Response(
                {"error": "Seat is already booked at this time"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return super().create(request, *args, **kwargs)
