from rest_framework import serializers

from manuals.models import City


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = (
            "id",
            "name",
            "description",
        )


class MasterTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = (
            "id",
            "name",
            "description",
        )