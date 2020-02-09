from django.utils.datetime_safe import datetime
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# from personal_account.custom_permissions import IsActivePermission
from manuals.models import MasterType, City
from order.serializers import OrderSerializer
from personal_account.models import get_user, ClientAccount, MasterAccount
from order.models import Order, OrderStatus
from photos.models import Photo


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        user = get_user(request)
        if isinstance(user, dict):
            return Response(user)

        client = ClientAccount.objects.get(user=user)
        # order_form = OrderForm(request.POST)
        # if order_form.is_valid():
        city = City.objects.get(id=int(request.POST.get('city')))
        master_type = MasterType.objects.get(id=request.POST.get('master_type'))
        status_code = OrderStatus.objects.get(code="sm")
        date_from = datetime.utcfromtimestamp(
            int(request.POST.get('request_date_from')))
        date_to = datetime.utcfromtimestamp(
            int(request.POST.get('request_date_to')))
        request_date_from = date_from
        request_date_to = date_to
        description = request.POST.get('description')
        order = Order(
                client=client,
                city=city,
                master_type=master_type,
                request_date_from=request_date_from,
                request_date_to=request_date_to,
                status_code=status_code,
                description=description,)
        order.save()
        # Что делать с одинаковыми названиями файлов?
        # (Хотя джанго это вроде учитывает)

        for key, file in request.FILES.items():
            photo = Photo(user=user, image=file)
            photo.save()
            order.photo.add(photo)
        return Response(status=HTTP_200_OK)

    @staticmethod
    def get(request):
        user = get_user(request)
        if isinstance(user, dict):
            return Response(user)
        if (MasterAccount.objects.filter(user=user).exists() and
                not ClientAccount.objects.filter(user=user).exists()):
            status_code = OrderStatus.objects.get(code="sm")
            orders = Order.objects.filter(status_code=status_code)
        elif (ClientAccount.objects.filter(user=user).exists() and
                not MasterAccount.objects.filter(user=user).exists()):
            client = ClientAccount.objects.get(user=user)
            orders = Order.objects.filter(client=client)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)
        orders = OrderSerializer(orders, many=True)
        return Response({"orders": orders.data}, status=HTTP_200_OK)


class OrderById(APIView):

    @staticmethod
    def patch(request, order_id):
        # ToDo
        return Response(status=HTTP_200_OK)

    @staticmethod
    def get(request, order_id):
        # ToDo
        content = {"id": order_id, "town": "Москва", "masterType": "Парикмахер",
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
