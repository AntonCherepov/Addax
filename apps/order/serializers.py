from rest_framework.serializers import ModelSerializer

from order.models import Order
from photos.serializers import PhotoSerializer


class OrderSerializer(ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True, source='photo')

    class Meta:
        model = Order
        exclude = ("photo",)
