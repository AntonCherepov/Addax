from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from manuals.models import (City, MasterType)
from manuals.serializers import CitySerializer, MasterTypeSerializer


class CityView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        cities = City.objects.all()
        serialized_cities = CitySerializer(cities, many=True)
        return Response({"towns": serialized_cities.data}, status=HTTP_200_OK)


class MasterTypeView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        masters_types = MasterType.objects.all()
        serialized_masters = MasterTypeSerializer(masters_types, many=True)
        return Response({"masters_types": serialized_masters.data},
                        status=HTTP_200_OK)
