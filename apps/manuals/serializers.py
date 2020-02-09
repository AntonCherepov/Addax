from rest_framework.serializers import ModelSerializer

from manuals.models import City


class CitySerializer(ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"


class MasterTypeSerializer(ModelSerializer):

    class Meta:
        model = City
        fields = "__all__"
