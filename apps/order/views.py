from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.utils.datetime_safe import datetime as dt
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                                   HTTP_201_CREATED, HTTP_403_FORBIDDEN)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from config.constants import IMAGE_EXTENSIONS
from manuals.models import MasterType, City
from order.forms import OrderForm
from order.serializers import OrderSerializer
from personal_account.custom_permissions import IsConfirmed
from personal_account.models import get_user, ClientAccount, MasterAccount
from order.models import Order, OrderStatus
from photos.models import Photo


class OrderView(APIView):
    permission_classes = (IsAuthenticated, IsConfirmed)

    @staticmethod
    def post(request):
        user = get_user(request)
        if isinstance(user, dict):
            return Response(status=HTTP_400_BAD_REQUEST)
        try:
            client = ClientAccount.objects.get(user=user)
        except ObjectDoesNotExist:
            return Response(status=HTTP_403_FORBIDDEN)
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            city = City.objects.get(id=request.POST.get('city_id'))
            master_type_id = MasterType.objects.get(
                id=request.POST.get('master_type_id'))
            status_code = OrderStatus.objects.get(code="sm")
            request_date_from = dt.utcfromtimestamp(
                int(request.POST.get('request_date_from')))
            request_date_to = dt.utcfromtimestamp(
                int(request.POST.get('request_date_to')))
            description = request.POST.get('description')
            order = Order(
                client=client,
                city=city,
                master_type=master_type_id,
                request_date_from=request_date_from,
                request_date_to=request_date_to,
                status_code=status_code,
                description=description, )
            order.save()
            files = request.FILES
            image_keys = list(filter(
                lambda k: str(files[k]).endswith(IMAGE_EXTENSIONS),
                files.keys()
            )
            )
            for key in image_keys[:5:]:
                photo = Photo(user=user, image=files[key])
                photo.save()
                order.photo.add(photo)
            order = OrderSerializer(order)
            return Response({"order": order.data}, status=HTTP_201_CREATED)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

    @staticmethod
    def get(request):
        user = get_user(request)
        if isinstance(user, dict):
            return Response(user)

        last_updates = request.GET.get("last_updates")
        order_status = request.GET.get("order_status")
        limit = request.GET.get("limit")
        offset = request.GET.get("offset")
        if (MasterAccount.objects.filter(user=user).exists() and
                not ClientAccount.objects.filter(user=user).exists()):
            master = MasterAccount.objects.get(user=user)
            orders = Order.objects.filter(
                Q(status_code="sm") | Q(reply__master=master)
            )

        elif (ClientAccount.objects.filter(user=user).exists() and
              not MasterAccount.objects.filter(user=user).exists()):
            client = ClientAccount.objects.get(user=user)
            orders = Order.objects.filter(client=client)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
        try:
            if order_status:
                orders = orders.filter(status_code=order_status)
            if last_updates:
                update = dt.utcfromtimestamp(int(last_updates))
                orders = orders.filter(date_modified__gt=update)
            if offset:
                orders = orders[int(offset)::]
            if limit:
                orders = orders[:int(limit):]
        except (ValueError, OSError):
            return Response(status=HTTP_400_BAD_REQUEST)
        except AssertionError as e:
            if str(e) == "Negative indexing is not supported.":
                return Response(status=HTTP_400_BAD_REQUEST)

        orders = OrderSerializer(orders, many=True)
        try:
            return Response({"orders": orders.data}, status=HTTP_200_OK)
        except IntegrityError:
            return Response(status=HTTP_400_BAD_REQUEST)


class OrderById(APIView):

    @staticmethod
    def patch(request, order_id):
        # ToDo
        return Response(status=HTTP_200_OK)

    @staticmethod
    def get(request, order_id):
        # ToDo
        content = {"id": order_id, "town": "Москва",
                   "masterType": "Парикмахер",
                   "status": "active", "creationDate": 1579077441,
                   "requestDateFrom": 1579077452, "requestDateTo": 1579077453,
                   "description": "", "selectionDate": 1579077453,
                   "photos": [["/media/lol.jpg", "/media/lol_thumb.jpg"],
                              ["/media/abc.jpg", "/media/abc_thumb.jpg"]
                              ],
                   "responses": [{"id": 5,
                                  "proposedDateFrom": 123123,
                                  "proposedDateTo": 123124,
                                  "comment": "AAA",
                                  "cost": 7500,
                                  "creationDate": 123122,
                                  "status": "Рассматривается!",
                                  "master": {
                                      "id": 123,
                                      "name": "Салон №215",
                                      "avatar": "/media/lul.jpg",
                                      "avatar_small": "/media/lul_thumb.jpg"
                                  }}]}

        return Response(content, status=HTTP_200_OK)


class Replies(APIView):

    @staticmethod
    def post(request, order_id):
        # ToDo
        content = {"id": 5,
                   "order_id": order_id,
                   "suggested_time_from": 123123,
                   "suggested_time_to": 123124,
                   "comment": "AAA",
                   "cost": 7500,
                   "creationDate": 123122,
                   "status": "Рассматривается!",
                   "master_id": 123}
        return Response(content, status=HTTP_200_OK)

    @staticmethod
    def get(request):
        # ToDo
        content = [{"id": 5,
                    "suggested_time_from": 123123,
                    "suggested_time_to": 123124,
                    "comment": "AAA",
                    "cost": 7500,
                    "creationDate": 123122,
                    "status": "Рассматривается!",
                    "master": {
                        "id": 123,
                        "name": "Салон №215",
                        "avatar": "/media/lul.jpg",
                        "avatar_small": "/media/lul_thumb.jpg"
                    }}]
        return Response(content, status=HTTP_200_OK)
