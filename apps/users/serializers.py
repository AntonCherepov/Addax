from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from albums.models import Album
from config.constants import AVATAR, MASTER_GALLERY, MASTER_WORKPLACE
from core.serializers import DynamicFieldsModelSerializer
from users.models import User, MasterAccount


class BaseMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = MasterAccount
        exclude = ('user',)

    avatar_album_id = SerializerMethodField('get_avatar_album')
    gallery_album_id = SerializerMethodField('get_gallery_album')
    workplace_album_id = SerializerMethodField('get_workplace_album')
    feedbacks_information = SerializerMethodField('get_feedback_information')

    def get_album(self, obj, album_type):
        try:
            album = Album.objects.get(user=obj.user.id,
                                      type=album_type)
            return album.id
        except ObjectDoesNotExist:
            return

    def get_avatar_album(self, obj):
        return self.get_album(obj, AVATAR)

    def get_gallery_album(self, obj):
        return self.get_album(obj, MASTER_GALLERY)

    def get_workplace_album(self, obj):
        return self.get_album(obj, MASTER_WORKPLACE)

    def get_feedback_information(self, obj):
        from feedbacks.models import FeedBack
        feedbacks = FeedBack.objects.filter(master=obj)
        average_rating = feedbacks.aggregate(Avg('rating'))['rating__avg']
        count = feedbacks.count()
        info = {'average_rating': average_rating, 'count': count}
        return info

    def get_email(self, obj):
        return obj.user.email


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('type_code', 'status')


class MasterSerializer(DynamicFieldsModelSerializer, BaseMasterSerializer):

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        request = context.get('request')
        fields = request.GET.get('master_fields', None) if request else None
        kwargs['fields'] = fields
        kwargs['exclude_fields'] = context.get('master_exclude_fields', set())
        super(MasterSerializer, self).__init__(*args, **kwargs)


class UserMasterSerializer(DynamicFieldsModelSerializer):
    master = SerializerMethodField('get_master_serializer')

    class Meta:
        model = User
        fields = ('type_code', 'status', 'master')

    def get_master_serializer(self, obj):
        serializer = MasterSerializer(obj.masteraccount,
                                      context=self.context)
        return serializer.data


class UserClientSerializer(serializers.ModelSerializer):

    client_id = SerializerMethodField('get_client_id')

    class Meta:
        model = User
        fields = ('type_code', 'status', 'client_id')

    def get_client_id(self, obj):
        return obj.clientaccount.id


class MasterAccountOwnerSerializer(BaseMasterSerializer):

    phone = SerializerMethodField('get_phone_number')
    balance = SerializerMethodField('get_balance')
    email = SerializerMethodField('get_email')

    class Meta:
        model = MasterAccount
        exclude = ('user',)

    def get_phone_number(self, obj):
        return obj.user.phone_number

    def get_balance(self, obj):
        return obj.user.balance.current_value

    def get_email(self, obj):
        return obj.user.email
