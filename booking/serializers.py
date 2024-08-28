from datetime import datetime

from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Booking, Seat, Venue


class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = ["id", "name", "address"]

    def validate_name(self, name: str) -> str:
        if Venue.objects.filter(name=name).exists():
            raise ValidationError(f'Venue already exists with the name "{name}"')
        return name


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "venue", "seat_number"]

    def validate(self, data: dict) -> dict:
        # Assuming `guest_name`, `booking_date`, and `seat` are passed in the data
        seat_number = self.context["request"].data.get("seat_number")
        venue = data.get("venue")

        if Seat.objects.filter(venue=venue, seat_number=seat_number).exists():
            raise ValidationError("The same venue can't have duplicate seat")
        return data


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "seat",
            "guest_name",
            "booking_date",
            "booking_time",
            "created_at",
        ]

    # Validate the booking data before saving it to the database.
    def validate(self, data: dict) -> dict:
        booking_date = self.context["request"].data.get("booking_date")
        booking_time = self.context["request"].data.get("booking_time")
        seat_id = self.context["request"].data.get("seat")
        seat = Seat.objects.get(id=seat_id)
        guest_name = self.context["request"].data.get("guest_name")

        # Check if the seat is already booked
        if Booking.objects.filter(
            seat=seat, booking_date=booking_date, guest_name=guest_name
        ).exists():
            raise serializers.ValidationError("Seat is already booked at this time.")

        # Check if booking_date or booking_time is None
        if booking_date is None:
            raise ValidationError({"booking_date": "Booking date cannot be None."})
        if booking_time is None:
            raise ValidationError({"booking_time": "Booking time cannot be None."})

        # Check if booking date is in the future
        now = datetime.now()
        if datetime.strptime(booking_date, "%Y-%m-%d").date() <= now.date():
            raise serializers.ValidationError("Booking date must be in the future.")

        # Check if booking time is in the future
        if datetime.strptime(booking_time, "%H:%M:%S").time() <= now.time():
            raise serializers.ValidationError("Booking time must be in the future.")

        # Check if the guest name is not empty
        if not guest_name:
            raise serializers.ValidationError("Guest name cannot be empty.")

        # Check if the guest already booked the seat for the same venue
        if Booking.objects.filter(
            guest_name=guest_name, seat__venue=seat.venue
        ).exists():
            raise serializers.ValidationError(
                f"Guest '{guest_name}' already booked"
                f" a seat at venue '{seat.venue.name}'"
            )
        return super().validate(data)
