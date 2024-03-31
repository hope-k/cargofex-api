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
    serializer_class = serializers.UserSerializer

    def post(self, request, *args, **kwargs):

        with transaction.atomic():
            # check if username and email already exist
            if User.objects.filter(username=request.data.get("username")).exists():
                raise ValidationError("Username already exists")
            if User.objects.filter(email=request.data.get("email")).exists():
                raise ValidationError("Email already exists")

            user_data = {
                "username": request.data.get("username"),
                "email": request.data.get("email"),
                "password": request.data.get("password"),
                "is_staff": False,
                "is_active": True,
                "is_superuser": False,
            }

            user_data["password"] = make_password(user_data["password"])
            user_serializer = serializers.UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
            additional_info_data = {
                "full_name": request.data.get("full_name"),
                "phone": request.data.get("phone"),
                "address": request.data.get("address"),
                "company": request.data.get("company"),
                "job_title": request.data.get("job_title"),
                "user": user,
            }
            print(additional_info_data)
            AdditionalInfo.objects.create(**additional_info_data)

            return Response(user_serializer.data, status=status.HTTP_201_CREATED)


# class ItemViewSet(NestedViewSetMixin, ModelViewSet):
#     queryset = models.Item.objects.all()
#     serializer_class = serializers.ItemSerializer


# class TrackingViewSet(NestedViewSetMixin, ModelViewSet):
#     queryset = models.Tracking.objects.all()
#     serializer_class = serializers.TrackingSerializer
