from rest_framework.serializers import Serializer, ImageField


class PhotoSerializer(Serializer):
    image_thumb = ImageField(read_only=True)
    image = ImageField(read_only=True)
