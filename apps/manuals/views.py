from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from manuals.models import (City, OrderStatus, ReplyStatus,
                            UserStatus, MasterStatus, MasterType, UserType)
from manuals.serializers import CitySerializer, MasterTypeSerializer


def creator():
    City(name="Воронеж").save()
    OrderStatus.objects.bulk_create(
        [OrderStatus(code="sm", name="Подбор мастеров"),
         OrderStatus(code="ms", name="Выбран мастер"),
         OrderStatus(code="сс", name="Отменена клиентом"),
         OrderStatus(code="cm", name="Отменена мастером"),
         OrderStatus(code="na", name="Клиент не приехал"),
         OrderStatus(code="cs", name="Завершена успешно")])
    UserType.objects.bulk_create([UserType(code="c", name="client"),
                                  UserType(code="m", name="master")])
    UserStatus.objects.bulk_create([UserStatus(code="rg", name="registered"),
                                    UserStatus(code="cf", name="confirmed"),
                                    UserStatus(code="bn", name="banned")])
    MasterType.objects.bulk_create(
        [MasterType(name="Визажист"),
         MasterType(name="Косметолог"),
         MasterType(name="Массажист"),
         MasterType(name="Мастер по маникюру"),
         MasterType(name="Мастер по наращиванию ресниц"),
         MasterType(name="Парикмахер"),
         MasterType(name="Мастер эпиляции")])
    MasterStatus.objects.bulk_create([MasterStatus(code="vr", name="verified"),
                                      MasterStatus(code="uv", name="unverified"),
                                      MasterStatus(code="bn", name="banned")])
    ReplyStatus.objects.bulk_create(
        [ReplyStatus(code="sl", name="Выбран"),
         ReplyStatus(code="cs", name="Рассматривается"),
         ReplyStatus(code="rj", name="Отклонен"),
         ReplyStatus(code="rc", name="Отозван")])


class CityView(APIView):
    # permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        cities = City.objects.all()
        serialized_cities = CitySerializer(cities, many=True)
        return Response({"towns": serialized_cities.data}, status=HTTP_200_OK)


class MasterTypeView(APIView):
    # permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        # creator()
        masters_types = MasterType.objects.all()
        serialized_masters = MasterTypeSerializer(masters_types, many=True)
        return Response({"masters_types": serialized_masters.data},
                        status=HTTP_200_OK)
