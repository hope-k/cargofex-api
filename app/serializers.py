from rest_framework import serializers
from . import models
from users import models as user_models


class UserAdditionalInfoSerializer(serializers.ModelSerializer):
    #make user field hidden
    class Meta:
        model = user_models.AdditionalInfo
        exclude = ["user"]


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        exclude = ["shipment"]


class UserSerializer(serializers.ModelSerializer):
    additional_info = UserAdditionalInfoSerializer(required=False)
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(
        required=True,
    )
    email = serializers.EmailField(
        required=True,
    )

    class Meta:
        model = user_models.User
        fields = ["id", "username", "email", "additional_info", "password"]

      
        


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        exclude = ["shipment"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = "__all__"


class TrackingSerializer(serializers.ModelSerializer):
    statusText = serializers.CharField(source="get_status_display", read_only=True)
    location = LocationSerializer()

    class Meta:
        model = models.Tracking
        exclude = ["shipment"]
        ordering = ["-created_at"]
        depth = 1


class ShipmentSerializer(serializers.ModelSerializer):
    tracking_log = TrackingSerializer(
        many=True,
        read_only=True,
    )
    origin = LocationSerializer()
    destination = LocationSerializer()
    statusText = serializers.CharField(source="get_status_display", read_only=True)
    manager = UserSerializer()
    notifications = NotificationSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = models.Shipment
        fields = "__all__"
        depth = 1
