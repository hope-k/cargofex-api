from rest_framework import serializers
from . import models
from users import models as user_models
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model


User = get_user_model()


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
    # Ensure username and email are required and unique
    username = serializers.CharField(
        required=True,
        # Validator checks uniqueness during is_valid()
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that username already exists.",
            )
        ],
    )
    email = serializers.EmailField(
        required=True,
        # Validator checks uniqueness during is_valid()
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that email already exists.",
            )
        ],
    )

    def create(self, validated_data):
        # Use create_user which handles password hashing automatically
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            # create_user also sets is_active=True and staff/superuser=False
        )
        return user

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
