from rest_framework.serializers import ModelSerializer

from order.models import Order
from photos.serializers import PhotoSerializer
from manuals.serializers import CitySerializer, MasterTypeSerializer


class OrderSerializer(ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True, source='photo')
    city = CitySerializer(read_only=True)
    master_type = MasterTypeSerializer(read_only=True)

    class Meta:
        model = Order
        exclude = ("photo",)
