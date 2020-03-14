from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from order.models import Order, Reply
from photos.serializers import PhotoSerializer


class OrderSerializer(ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True, source='photo')
    city = SerializerMethodField('get_city_name')
    master_type = SerializerMethodField('get_master_type_name')
    status = SerializerMethodField('get_status_name')

    @staticmethod
    def get_city_name(obj):
        return obj.city.name

    @staticmethod
    def get_master_type_name(obj):
        return obj.master_type.name

    @staticmethod
    def get_status_name(obj):
        return obj.status_code.name

    class Meta:
        model = Order
        exclude = ("photo", "status_code", "client")


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
