# Generated by Django 5.1 on 2024-08-28 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0009_remove_booking_unique_booking_per_time_slot_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="venue",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
