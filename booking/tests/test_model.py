from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from booking.models import Booking, Seat, Venue


class BookingTestCase(TestCase):
    def setUp(self) -> None:
        self.venue = Venue.objects.create(name="Test Venue", address="123 Test St")
        self.seat = Seat.objects.create(venue=self.venue, seat_number="A1")
        self.booking_time = timezone.now() + timedelta(days=1)

    def test_create_valid_booking(self) -> None:
        Booking.objects.create(
            seat=self.seat,
            guest_name="John Doe",
            booking_date=self.booking_time.date(),
            booking_time=self.booking_time.time(),
        )
        self.assertEqual(Booking.objects.count(), 1)

    def test_prevent_double_booking(self) -> None:
        Booking.objects.create(
            seat=self.seat,
            guest_name="John Doe",
            booking_date=self.booking_time.date(),
            booking_time=self.booking_time.time(),
        )
        # Attempt to create a second booking for the same user, same seat, same date
        duplicate_booking = Booking(
            seat=self.seat,
            guest_name="John Doe",
            booking_date=self.booking_time.date(),
            booking_time=(self.booking_time + timedelta(hours=1)).time(),
        )

        # Check for the ValidationError
        with self.assertRaises(ValidationError):
            duplicate_booking.full_clean()
            duplicate_booking.save()

    def test_booking_with_invalid_seat_id(self) -> None:
        with self.assertRaises(Seat.DoesNotExist):
            invalid_seat = Seat.objects.get(pk=9999)
            Booking.objects.create(
                seat=invalid_seat,
                guest_name="Invalid Seat",
                booking_date=self.booking_time.date(),
                booking_time=self.booking_time.time(),
            )

    def test_booking_without_seat(self) -> None:
        with self.assertRaises(IntegrityError):
            Booking.objects.create(
                guest_name="No Seat",
                booking_date=self.booking_time.date(),
                booking_time=self.booking_time.time(),
            )

    def test_booking_in_the_past(self) -> None:
        past_time = timezone.now() - timedelta(days=1)
        with self.assertRaises(ValidationError):
            booking = Booking(
                seat=self.seat,
                guest_name="Past Booking",
                booking_date=past_time.date(),
                booking_time=past_time.time(),
            )
            booking.full_clean()
            booking.save()

    def test_multiple_bookings_same_day_different_times(self) -> None:
        Booking.objects.create(
            seat=self.seat,
            guest_name="John Doe",
            booking_date=self.booking_time.date(),
            booking_time=self.booking_time.time(),
        )
        later_time = self.booking_time + timedelta(hours=2)
        Booking.objects.create(
            seat=self.seat,
            guest_name="John",
            booking_date=self.booking_time.date(),
            booking_time=later_time.time(),
        )
        self.assertEqual(Booking.objects.count(), 2)


class VenueTestCase(TestCase):
    def test_create_valid_venue(self) -> None:
        Venue.objects.create(name="Valid Venue", address="123 Test St")
        self.assertEqual(Venue.objects.count(), 1)

    def test_prevent_duplicate_venue_names(self) -> None:
        Venue.objects.create(name="Unique Venue", address="123 Test St")
        with self.assertRaises(IntegrityError):
            Venue.objects.create(name="Unique Venue", address="789 Test Ave")

    def test_venue_name_length(self) -> None:
        short_name = "V"
        long_name = "V" * 101
        Venue.objects.create(name=short_name, address="123 Test St")
        Venue.objects.create(name=long_name, address="456 Test Ave")
        self.assertEqual(Venue.objects.count(), 2)


class SeatTestCase(TestCase):
    def setUp(self) -> None:
        self.venue1 = Venue.objects.create(name="Venue 1", address="123 Test St")
        self.venue2 = Venue.objects.create(name="Venue 2", address="456 Test St")

    def test_create_valid_seat(self) -> None:
        Seat.objects.create(venue=self.venue1, seat_number="A1")
        self.assertEqual(Seat.objects.count(), 1)

    def test_create_seat_with_duplicate_seat_number_same_venue(self) -> None:
        Seat.objects.create(venue=self.venue1, seat_number="A1")
        with self.assertRaises(IntegrityError):
            Seat.objects.create(venue=self.venue1, seat_number="A1")

    def test_create_seat_with_duplicate_seat_number_different_venues(self) -> None:
        Seat.objects.create(venue=self.venue1, seat_number="A1")
        Seat.objects.create(venue=self.venue2, seat_number="A1")
        self.assertEqual(Seat.objects.count(), 2)
