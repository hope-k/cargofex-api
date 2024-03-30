import random
from django.db import models
import uuid
from cloudinary_storage.storage import MediaCloudinaryStorage


STATUS_CHOICES = (
    ("preparing", "Preparing"),
    ("in_transit", "In Transit"),
    ("delivered", "Delivered"),
    ("returned", "Returned"),
    ("delayed", "Delayed"),
    ("on_hold", "On Hold"),
)

LOGISTICS_CHOICES = (
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
)


def generate_tracking_number():
    tracking_number = "1ZCF"
    tracking_number += str(uuid.uuid4().int)[
        :10
    ]  # Extracts the first 10 characters of the integer representation of the UUID
    return tracking_number


class LogisticCompany(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        choices=LOGISTICS_CHOICES,
        default="Other",
        verbose_name="Logistic Company",
    )

    class Meta:
        verbose_name = "Logistic Company"
        verbose_name_plural = "Logistic Companies"

    def __str__(self):
        return self.name


class Location(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    latitude = models.FloatField(
        help_text="Get the latitude and longitude from Google Maps - gps-coordinates.net"
    )
    longitude = models.FloatField()

    class Meta:
        unique_together = ("latitude", "longitude")
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return f"City: {self.city}, State:{self.state}, Address: {self.address}"


class Shipment(models.Model):

    tracking_number = models.CharField(
        max_length=255,
        unique=True,
        default=generate_tracking_number,
        verbose_name="Tracking Number",
        help_text="Unique tracking number for the package(Automatically generated )",
    )
    origin = models.ForeignKey(
        Location,
        related_name="shipment_origin",
        on_delete=models.CASCADE,
        verbose_name="Origin(From)",
    )
    destination = models.ForeignKey(
        Location,
        related_name="shipment_destination",
        on_delete=models.CASCADE,
        verbose_name="Destination(To)",
        help_text="The destination of the package/receiver's address",
    )
    receiver_name = models.CharField(max_length=255, blank=True, null=True)
    receiver_phone = models.CharField(max_length=255, blank=True, null=True)

    departure = models.DateTimeField()
    est_arrival = models.DateTimeField()
    total_est = models.FloatField(
        help_text="Total estimated cost of the shipment(eg. 100.50)"
    )
    total_weight = models.FloatField(
        help_text="Total weight of the shipment in KGs(eg. 10.5)"
    )
    manager = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="shipments",
        verbose_name="Package Manager",
        blank=True,
        null=True,
        help_text=(
            "The user controlling this package from admin panel.\n"
            "Contact Super Admin to assign you as a manager for the package you're creating if you're not assigned as a manager already."
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"
        unique_together = ("tracking_number", "origin", "destination")

    def __str__(self):
        return f"Package {self.pk} FROM: {self.origin.address} TO: {self.destination.address}"


class Tracking(models.Model):
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="preparing"
    )
    shipment = models.ForeignKey(
        Shipment,
        related_name="tracking_log",
        on_delete=models.CASCADE,
        verbose_name="Package",
        help_text="The package being tracked",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Current Location",
        help_text="e.g. Warehouse, Airport etc.",
    )
    message = models.TextField(
        blank=True,
        null=True,
        help_text="e.g. Out for delivery etc",
        verbose_name="Tracking Message(If any)",
    )
    logistics_company = models.ForeignKey(
        LogisticCompany,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Logistic Company",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Package Tracking Event Log"
        verbose_name_plural = "Packages Tracking Event Logs"
        unique_together = (
            "shipment",
            "location",
            "status",
        )

    def __str__(self):
        return f" Tracking: {self.shipment} currently at {self.location}"


class Image(models.Model):

    image = models.ImageField(
        upload_to="package_images",
        verbose_name="Package Image",
        help_text="Image of the package",
        storage=MediaCloudinaryStorage(),
    )
    name = models.CharField(max_length=255, blank=True, null=True)
    shipment = models.ForeignKey(
        Shipment,
        related_name="images",
        on_delete=models.CASCADE,
        verbose_name="Package Item",
        blank=True,
        null=True,
        
    )

    class Meta:
        verbose_name = "Packace Item Image"
        verbose_name_plural = "Package Item Images"

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.storage.delete(self.image.name)
        super().delete(*args, **kwargs)


class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    shipment = models.ForeignKey(
        Shipment,
        related_name="notifications",
        on_delete=models.CASCADE,
        verbose_name="Package",
    )

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return self.title
    

