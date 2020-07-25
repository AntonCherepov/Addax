from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

from core.exceptions import RequestUserError
from users.models import User


def get_token(request) -> Token:
    try:
        token_raw = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        token = Token.objects.get(key=token_raw)
    except ObjectDoesNotExist:
        raise RequestUserError('Token does not exist.')
    except KeyError:
        raise RequestUserError('No token in request.')
    return token


def get_user_by_token(token) -> User:
    try:
        user = User.objects.get(id=token.user_id)
    except ObjectDoesNotExist:
        raise RequestUserError('User does not exist.')
    return user


def get_user(request) -> User:
    token = get_token(request)
    if user := get_user_by_token(token):
        return user
    raise RequestUserError('User is None.')


