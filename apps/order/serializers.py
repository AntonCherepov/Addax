from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from order.models import Order, Reply
from photos.serializers import PhotoSerializer
from manuals.serializers import CitySerializer, MasterTypeSerializer


class OrderSerializer(ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True, source='photo')
    city = CitySerializer(read_only=True)
    master_type = MasterTypeSerializer(read_only=True)

    class Meta:
        model = Order
        exclude = ("photo",)


class ReplySerializer(ModelSerializer):
    master_id = SerializerMethodField('get_master_id')
    order_id = SerializerMethodField('get_order_id')
    status = SerializerMethodField('get_status_name')

    class Meta:
        model = Reply
        exclude = ("master", "order", "date_modified")

    @staticmethod
    def get_master_id(obj):
        return obj.master.id

    @staticmethod
    def get_order_id(obj):
        return obj.order.id

    @staticmethod
    def get_status_name(obj):
        return obj.status.name
