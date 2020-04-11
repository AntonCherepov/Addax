from rest_framework.fields import SerializerMethodField

from core.serializers import DynamicFieldsModelSerializer
from orders.models import Order, Reply
from users.serializers import MasterSerializer


class ReplySerializer(DynamicFieldsModelSerializer):

    master_id = SerializerMethodField('get_master_id')
    order_id = SerializerMethodField('get_order_id')
    status = SerializerMethodField('get_status_name')
    master = SerializerMethodField('get_master_serializer')

    class Meta:
        model = Reply
        exclude = ("order", "date_modified")

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        request = context.get('request')
        fields = request.GET.get('reply_fields', None) if request else None
        kwargs['fields'] = fields
        kwargs['exclude_fields'] = context.get('reply_exclude_fields')
        super(ReplySerializer, self).__init__(*args, **kwargs)

    def get_master_serializer(self, obj):
        serializer = MasterSerializer(obj.master,
                                      context=self.context)
        return serializer.data

    def get_master_id(self, obj):
        return obj.master.id

    def get_order_id(self, obj):
        return obj.order.id

    def get_status_name(self, obj):
        return obj.status.name


class OrderSerializer(DynamicFieldsModelSerializer):

    city = SerializerMethodField('get_city_name')
    master_type = SerializerMethodField('get_master_type_name')
    status = SerializerMethodField('get_status_name')
    album_id = SerializerMethodField('get_album_id')
    replies = SerializerMethodField('get_replies_serializer')
    replies_count = SerializerMethodField('get_replies_count')

    class Meta:
        model = Order
        fields = [
            "id", "city",
            "master_type", "status",
            "album_id", "date_created",
            "request_date_from", "request_date_to",
            "description", "selection_date",
            "replies", "replies_count",
        ]

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        request = context.get('request')
        fields = request.GET.get('order_fields', None) if request else None
        kwargs['fields'] = fields
        kwargs['exclude_fields'] = context.get('order_exclude_fields')
        super(OrderSerializer, self).__init__(*args, **kwargs)

    def get_replies_serializer(self, obj):
        if master := self.context.get('master'):
            replies = obj.replies.filter(master=master)
        else:
            replies = obj.replies.all()
        serializer = ReplySerializer(replies,
                                     many=True,
                                     context=self.context)
        return serializer.data

    def get_replies_count(self, obj):
        return obj.replies.count()

    def get_city_name(self, obj):
        return obj.city.name

    def get_master_type_name(self, obj):
        return obj.master_type.name

    def get_status_name(self, obj):
        return obj.status_code.name

    def get_album_id(self, obj):
        return obj.album.id
