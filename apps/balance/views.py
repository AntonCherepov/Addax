from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from core.decorators import get_user_decorator
from users.permissions import IsMaster


class GetMasterBalance(APIView):

    permission_classes = (IsMaster, )

    @get_user_decorator
    def get(self, request, user):
        return Response({'balance': user.balance.current_value},
                        status=HTTP_200_OK)
