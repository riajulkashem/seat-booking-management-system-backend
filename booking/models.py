from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self) -> str:
        return self.name

    @property
    def total_seat_booked(self) -> int:
        return Booking.objects.filter(seat__venue=self).count()


class Seat(models.Model):
    venue = models.ForeignKey(Venue, related_name="seats", on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.venue.name} - {self.seat_number}"


class Booking(models.Model):
    seat = models.ForeignKey(Seat, related_name="bookings", on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=100, verbose_name="Guest Name")
    booking_date = models.DateField(verbose_name="Booking Date")
    booking_time = models.TimeField(verbose_name="Booking Time")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f"{self.guest_name} - {self.seat.seat_number} on "
            f"{self.booking_date} at {self.booking_time}"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["seat", "guest_name", "booking_date", "booking_time"],
                name="unique_booking",
            )
        ]
