from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# from personal_account.custom_permissions import IsActivePermission
from manuals.models import MasterType
from personal_account.models import get_user
from order.models import Order, OrderStatus


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        # ToDo
        return Response(status=HTTP_200_OK)

    @staticmethod
    def get(request):
        # ToDo
        content = {

            "orders": [
                {"id": 1, "town": "Москва", "masterType": "Парикмахер",
                 "status": "active", "creationDate": 1579077451,
                 "requestDateFrom": 1579077452, "requestDateTo": 1579077453,
                 "description": "", "selectionDate": 1579077453,
                 "photos": [["/media/lol.jpg", "/media/lol_thumb.jpg"],
                            ["/media/abc.jpg", "/media/abc_thumb.jpg"]
                            ]
                 }
            ]
        }

        return Response(content, status=HTTP_200_OK)


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
                   "reply_status": "Рассматривается!", # Возможно лучше status
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
