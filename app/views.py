from . import models
from rest_framework.viewsets import ModelViewSet, generics
from . import serializers
from users.models import User
from django_filters.rest_framework import DjangoFilterBackend
from .permission import ReadOnly
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from users.models import User, AdditionalInfo
from django.db import transaction


# from .filter import ShipmentFilter


class ShipmentViewSet(APIView):
    permission_classes = [ReadOnly]

    def get(self, request, *args, **kwargs):
        tracking_number = request.query_params.get("tracking_number")
        shipment = models.Shipment.objects.filter(
            tracking_number=tracking_number
        ).first()
        if not shipment:
            raise ValidationError(
                "Invalid Tacking Number. Please check the number and try again",
                code=status.HTTP_404_NOT_FOUND,
            )
        serializer = serializers.ShipmentSerializer(shipment)

        return Response(serializer.data)


class CreateUserView(APIView):
    """
    Handles user signup, creating both a User and their AdditionalInfo.
    Uses serializers EXCLUSIVELY for validation and data handling after instantiation.
    """

    # Define permission classes if needed, e.g., allow anyone to signup
    # permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request for user signup using serializers for validation.
        """
        # No preliminary checks using request.data.get() needed here anymore.
        # Serializers will handle required fields and uniqueness if configured.

        # Proceed with serializer-based processing within a transaction
        with transaction.atomic():
            # 1. Handle User creation using UserSerializer
            # Pass the request data directly.
            # Assumes UserSerializer is configured with required=True for fields
            # and UniqueValidators for username and email.
            # Also assumes UserSerializer handles password hashing in its .create() method.
            user_serializer = serializers.UserSerializer(data=request.data)
            user_serializer.is_valid(
                raise_exception=True
            )  # Performs all user field validation now
            user = user_serializer.save()  # Calls UserSerializer.create()

            # 2. Handle AdditionalInfo creation using UserAdditionalInfoSerializer
            # Pass the request data directly.
            additional_info_serializer = serializers.UserAdditionalInfoSerializer(data=request.data)
            additional_info_serializer.is_valid(
                raise_exception=True
            )  # Validates full_name, phone etc.
            # Provide the newly created user instance when saving the related info.
            additional_info_serializer.save(user=user)

            # 3. Prepare and return the response
            # Re-serialize the created user object to send back confirmed data (excluding password)
            response_data = user_serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
