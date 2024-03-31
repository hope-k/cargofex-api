# Generated by Django 5.0.3 on 2024-03-31 23:14

import app.models
import cloudinary_storage.storage
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        help_text="Image of the package",
                        storage=cloudinary_storage.storage.MediaCloudinaryStorage(),
                        upload_to="package_images",
                        verbose_name="Package Image",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "verbose_name": "Packace Item Image",
                "verbose_name_plural": "Package Item Images",
            },
        ),
        migrations.CreateModel(
            name="LogisticCompany",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("DHL", "DHL"),
                            ("FedEx", "FedEx"),
                            ("UPS", "UPS"),
                            ("USPS", "USPS"),
                            ("FedEx-Freight", "FedEx Freight"),
                            ("Aramex", "Aramex"),
                            ("UPS-Airlines", "UPS Airlines"),
                            ("DHL-Aviation", "DHL Aviation"),
                            ("FedEx-Express", "FedEx Express"),
                            ("USPS-Airlines", "USPS Airlines"),
                            ("TNT-Airways", "TNT Airways"),
                            ("Aramex-Aviation", "Aramex Aviation"),
                            ("Other", "Other"),
                        ],
                        default="Other",
                        max_length=255,
                        unique=True,
                        verbose_name="Logistic Company",
                    ),
                ),
            ],
            options={
                "verbose_name": "Logistic Company",
                "verbose_name_plural": "Logistic Companies",
            },
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Notification",
                "verbose_name_plural": "Notifications",
            },
        ),
        migrations.CreateModel(
            name="Tracking",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("preparing", "Preparing"),
                            ("in_transit", "In Transit"),
                            ("delivered", "Delivered"),
                            ("returned", "Returned"),
                            ("delayed", "Delayed"),
                            ("on_hold", "On Hold"),
                        ],
                        default="preparing",
                        max_length=50,
                    ),
                ),
                (
                    "message",
                    models.TextField(
                        blank=True,
                        help_text="e.g. Out for delivery etc",
                        null=True,
                        verbose_name="Tracking Message(If any)",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Package Tracking Event Log",
                "verbose_name_plural": "Packages Tracking Event Logs",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=255)),
                ("state", models.CharField(max_length=255)),
                ("country", models.CharField(max_length=255)),
                (
                    "latitude",
                    models.FloatField(
                        help_text="Get the latitude and longitude from Google Maps - gps-coordinates.net"
                    ),
                ),
                (
                    "longitude",
                    models.FloatField(
                        help_text="Make sure  your coordinates are valid as it will be used for the map."
                    ),
                ),
            ],
            options={
                "verbose_name": "Location",
                "verbose_name_plural": "Locations",
                "unique_together": {("latitude", "longitude")},
            },
        ),
        migrations.CreateModel(
            name="Shipment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tracking_number",
                    models.CharField(
                        default=app.models.generate_tracking_number,
                        help_text="Unique tracking number for the package(Automatically generated )",
                        max_length=255,
                        unique=True,
                        verbose_name="Tracking Number",
                    ),
                ),
                (
                    "receiver_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "receiver_phone",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("departure", models.DateTimeField()),
                ("est_arrival", models.DateTimeField()),
                (
                    "total_est",
                    models.FloatField(
                        help_text="Total estimated cost of the shipment(eg. 100.50)"
                    ),
                ),
                (
                    "total_weight",
                    models.FloatField(
                        help_text="Total weight of the shipment in KGs(eg. 10.5)"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "destination",
                    models.ForeignKey(
                        help_text="The destination of the package/receiver's address",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shipment_destination",
                        to="app.location",
                        verbose_name="Destination(To)",
                    ),
                ),
            ],
            options={
                "verbose_name": "Package",
                "verbose_name_plural": "Packages",
            },
        ),
    ]
