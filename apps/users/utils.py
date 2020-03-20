from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

from users.models import User


def get_token(request):
    try:
        token_raw = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
        token = Token.objects.get(key=token_raw)
    except ObjectDoesNotExist:
        return {"message": "ObjectDoesNotExist::Token", "status": False}
    except KeyError:
        return {"message": "KeyError::HTTP_AUTHORIZATION", "status": False}
    return token


def user_by_token(token):
    try:
        user = User.objects.get(id=token.user_id)
    except ObjectDoesNotExist:
        return {"message": "ObjectDoesNotExist::User", "status": False}
    return user


def get_user(request):
    t = get_token(request)
    if isinstance(t, Token):
        u = user_by_token(t)
        return u
    return
