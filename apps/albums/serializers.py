from rest_framework.serializers import Serializer, ImageField, IntegerField

from core.serializers import DynamicFieldsModelSerializer
from albums.models import Photo


class PhotoSerializer(Serializer):

    id = IntegerField()
    image_thumb = ImageField(read_only=True)
    image = ImageField(read_only=True)


class DynamicPhotoSerializer(DynamicFieldsModelSerializer):

    image_thumb = ImageField(read_only=True)

    class Meta:
        model = Photo
        exclude = ('user', 'album')
