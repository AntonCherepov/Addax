from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField

from albums.models import Album
from config.constants import AVATAR
from feedbacks.models import FeedBack
from orders.models import Order
from users.models import MasterAccount


class FeedBackSerializer(ModelSerializer):

    class Meta:
        model = FeedBack
        exclude = ('client', 'master')


class FeedbackNotificationOrderSerializer(ModelSerializer):

    date_finished = SerializerMethodField('get_selection_date')

    class Meta:
        model = Order
        fields = ('id', 'date_finished', 'master_type_id')

    def get_selection_date(self, obj):
        return obj.selection_date


class FeedbackNotificationMasterSerializer(ModelSerializer):

    avatar_album_id = SerializerMethodField('get_avatar_album')

    class Meta:
        model = MasterAccount
        fields = ('id', 'avatar_album_id', 'name')

    def get_album(self, obj, album_type):
        try:
            album = Album.objects.get(user=obj.user.id,
                                      type=album_type)
            return album.id
        except ObjectDoesNotExist:
            return

    def get_avatar_album(self, obj):
        return self.get_album(obj, AVATAR)


class FeedbackNotificationSerializer(ModelSerializer):
    order = SerializerMethodField('get_order_data')
    master = SerializerMethodField('get_master')

    class Meta:
        model = FeedBack
        fields = ('order', 'master')

    def get_order_data(self, obj):
        serializer = FeedbackNotificationOrderSerializer(obj.order)
        return serializer.data

    def get_master(self, obj):
        serializer = FeedbackNotificationMasterSerializer(obj.master)
        return serializer.data
