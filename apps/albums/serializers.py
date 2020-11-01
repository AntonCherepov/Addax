from rest_framework.serializers import Serializer, ImageField, IntegerField

from core.serializers import DynamicFieldsModelSerializer
from albums.models import Photo


class PhotoSerializer(Serializer):

    id = IntegerField()
    image_thumb = ImageField(read_only=True)
    image = ImageField(read_only=True)


class DynamicPhotoSerializer(DynamicFieldsModelSerializer):

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context', {})
        request = context.get('request')
        fields = request.GET.get('photos_fields', None) if request else None
        kwargs['fields'] = fields
        kwargs['exclude_fields'] = context.get('photos_exclude_fields')
        super(DynamicPhotoSerializer, self).__init__(*args, **kwargs)

    image_thumb = ImageField(read_only=True)

    class Meta:
        model = Photo
        exclude = ('user', 'album')
