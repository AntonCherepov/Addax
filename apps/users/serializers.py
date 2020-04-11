from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from albums.models import Album
from config.constants import AVATAR, MASTER_GALLERY, MASTER_WORKPLACE
from core.serializers import DynamicFieldsModelSerializer
from users.models import User, MasterAccount


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("type_code", "status_code")


class MasterSerializer(DynamicFieldsModelSerializer):

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        request = context.get('request')
        fields = request.GET.get('master_fields', None) if request else None
        kwargs['fields'] = fields
        kwargs['exclude_fields'] = context.get('master_exclude_fields', set())
        super(MasterSerializer, self).__init__(*args, **kwargs)

    avatar_album_id = SerializerMethodField('get_avatar_album')
    gallery_album_id = SerializerMethodField('get_gallery_album')
    workplace_album_id = SerializerMethodField('get_workplace_album')

    class Meta:
        model = MasterAccount
        exclude = ("user",)

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
