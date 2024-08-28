from django.contrib import admin
from .models import Venue, Seat, Booking


class BookingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["guest_name", "seat"]}),
        ("Date information", {"fields": ["booking_date", "booking_time"]}),
    ]
    list_display = ["guest_name", "seat", "booking_date", "booking_time"]
    list_filter = ["booking_date"]
    search_fields = ["guest_name", "seat__seat_number"]


class VenueAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "total_seat_booked"]


admin.site.register(Booking, BookingAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Seat)
admin.AdminSite.site_header = "Booking Management Administration"
