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



# from .filter import ShipmentFilter


class ShipmentViewSet(APIView):
    permission_classes = [ReadOnly]
    
    def get(self, request, *args, **kwargs):
        tracking_number = request.query_params.get('tracking_number')
        shipment = models.Shipment.objects.filter(tracking_number=tracking_number).first()
        if not shipment:
            raise ValidationError("Invalid Tacking Number. Please check the number and try again", code=status.HTTP_404_NOT_FOUND)
        serializer = serializers.ShipmentSerializer(shipment)
        
        return Response(serializer.data)
    
   
# class ItemViewSet(NestedViewSetMixin, ModelViewSet):
#     queryset = models.Item.objects.all()
#     serializer_class = serializers.ItemSerializer


# class TrackingViewSet(NestedViewSetMixin, ModelViewSet):
#     queryset = models.Tracking.objects.all()
#     serializer_class = serializers.TrackingSerializer
