from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.test import APITestCase

from booking.models import Booking, Seat, Venue


class VenueViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.valid_venue_data = {"name": "Test Venue", "address": "123 Test St"}
        self.invalid_venue_data = {"name": "", "address": "123 Test St"}
        self.venue = Venue.objects.create(**self.valid_venue_data)
        self.url = "/api/venues/"  # Adjust based on your URL routing

    def test_list_venues(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, [{"id": 1, "name": "Test Venue", "address": "123 Test St"}]
        )

    def test_create_venue_invalid(self) -> None:
        response = self.client.post(self.url, self.invalid_venue_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_venue_invalid(self) -> None:
        response = self.client.post(self.url, self.valid_venue_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        self.assertEqual(data["name"][0], "venue with this name already exists.")

    def test_create_venue(self) -> None:
        self.valid_venue_data["name"] = "New Venue"
        response = self.client.post(self.url, self.valid_venue_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Venue")

    def test_update_venue(self) -> None:
        response = self.client.put(
            f"{self.url}{self.venue.id}/",
            {"name": "Updated Venue", "address": "123 Test St"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Venue")

    def test_delete_venue(self) -> None:
        response = self.client.delete(f"{self.url}{self.venue.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"{self.url}{self.venue.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SeatViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.venue = Venue.objects.create(name="Test Venue", address="123 Test St")
        self.invalid_seat_data = {"seat_number": "A1", "venue": 9999}
        self.seat = Seat.objects.create(seat_number="A1", venue=self.venue)
        self.url = "/api/seats/"  # Adjust based on your URL routing

    def test_list_seats(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("A1", response.data[0]["seat_number"])

    def test_create_seat(self) -> None:
        response = self.client.post(
            self.url, {"seat_number": "A2", "venue": self.venue.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["seat_number"], "A2")

    def test_create_seat_invalid(self) -> None:
        response = self.client.post(self.url, self.invalid_seat_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_seat_in_same_venue(self) -> None:
        Seat.objects.create(seat_number="A2", venue=self.venue)
        response = self.client.post(
            self.url, {"seat_number": "A2", "venue": self.venue.id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["non_field_errors"][0],
            "The fields venue, seat_number must make a unique set.",
        )

    def test_update_seat(self) -> None:
        response = self.client.put(
            f"{self.url}{self.seat.id}/",
            {"seat_number": "B1", "venue": self.venue.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["seat_number"], "B1")

    def test_delete_seat(self) -> None:
        response = self.client.delete(f"{self.url}{self.seat.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"{self.url}{self.seat.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class BookingViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.venue = Venue.objects.create(name="Test Venue", address="123 Test St")
        self.seat = Seat.objects.create(seat_number="A1", venue=self.venue)
        self.booking_time = datetime.now() + timedelta(hours=1)
        self.valid_booking_data = {
            "seat": self.seat,
            "guest_name": "John Doe",
            "booking_date": "2054-08-28",
            "booking_time": self.booking_time.strftime("%H:%M:%S"),
        }
        self.invalid_booking_data = {
            "seat": self.seat,
            "guest_name": "John Doe",
            "booking_date": "2024-08-28",
            "booking_time": "10:00:00",
        }
        self.booking = Booking.objects.create(**self.valid_booking_data)
        self.url = "/api/bookings/"  # Adjust based on your URL routing

    def test_list_bookings(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, len(response.data))
        self.assertEqual("John Doe", response.data[0]["guest_name"])

    def test_create_booking(self) -> None:
        seat = Seat.objects.create(seat_number="A2", venue=self.venue)
        self.valid_booking_data["seat"] = seat.id
        self.valid_booking_data["guest_name"] = "New User"
        response = self.client.post(self.url, self.valid_booking_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data["guest_name"], self.valid_booking_data["guest_name"]
        )

    def test_create_booking_conflict(self) -> None:
        self.valid_booking_data["seat"] = self.seat.id
        response = self.client.post(self.url, self.valid_booking_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_update_booking(self) -> None:
        response = self.client.put(
            f"{self.url}{self.booking.id}/",
            {
                "seat": self.seat.id,
                "guest_name": "Riajul",
                "booking_date": "2054-08-28",
                "booking_time": self.booking_time.strftime("%H:%M:%S"),
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["guest_name"], "Riajul")

    def test_delete_booking(self) -> None:
        response = self.client.delete(f"{self.url}{self.booking.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"{self.url}{self.booking.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_booking_missing_field(self) -> None:
        # Test missing guest_name
        invalid_data = {
            "seat": self.seat.id,
            "booking_date": "2024-08-28",
            "booking_time": "10:00:00",
        }
        response = self.client.post(self.url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
