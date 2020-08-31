from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from core.exceptions import RequestUserError
from users import utils


def get_user_decorator(func):
    def wrapper(obj, request, *args, **kwargs):
        if bool(request.user and request.user.is_authenticated):
            try:
                user = utils.get_user(request)
                return func(obj, request, user, *args, **kwargs)
            except RequestUserError as e:
                return Response({'detail': str(e)},
                                status=HTTP_401_UNAUTHORIZED)
        return Response(status=HTTP_401_UNAUTHORIZED)
    return wrapper
