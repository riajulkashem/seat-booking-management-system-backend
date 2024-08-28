from rest_framework import serializers
from .models import Venue, Seat, Booking


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ["id", "name", "address"]


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "venue", "seat_number", "is_available"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "seat",
            "user_name",
            "booking_date",
            "booking_time",
            "created_at",
        ]
