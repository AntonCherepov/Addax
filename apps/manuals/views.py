from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from manuals.models import City
from manuals.serializers import CitySerializer, MasterTypeSerializer


class CityView(APIView):
    # permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        cities = City.objects.all()
        serialized_cities = CitySerializer(cities, many=True)
        return Response({"towns": serialized_cities.data}, status=HTTP_200_OK)


class MasterType(APIView):
    # permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        masters_types = MasterType.objects.all()
        serialized_masters = MasterTypeSerializer(masters_types, many=True)
        return Response({"masters_types": serialized_masters.data},
                        status=HTTP_200_OK)
