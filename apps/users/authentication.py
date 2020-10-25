import rest_framework.authentication

from users.models import MultiToken


class TokenAuthentication(rest_framework.authentication.TokenAuthentication):
    model = MultiToken
