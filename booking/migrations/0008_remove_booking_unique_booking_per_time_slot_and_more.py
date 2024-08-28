# Generated by Django 5.1 on 2024-08-28 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0007_remove_booking_unique_booking_per_user_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="booking",
            name="unique_booking_per_time_slot",
        ),
        migrations.AddConstraint(
            model_name="booking",
            constraint=models.UniqueConstraint(
                fields=("seat", "booking_date", "guest_name"),
                name="unique_booking_per_time_slot",
            ),
        ),
    ]
