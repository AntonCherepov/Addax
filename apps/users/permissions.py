from rest_framework.permissions import BasePermission

from users.utils import get_user


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsConfirmed(BasePermission):
    """
    Allows access only to confirmed users.
    """

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            user = get_user(request)
            if user is not None:
                return user.is_confirmed()
        return False


class IsNotBanned(BasePermission):
    """
    Allows access only to not banned users.
    """

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            user = get_user(request)
            if user is not None:
                return not user.is_banned()
        # user can't be banned if he is not authenticated
        return True


class MasterReadOnly(BasePermission):
    """
    Allows read only access for masters.
    """

    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated):
            user = get_user(request)
            if request.method in SAFE_METHODS or not user.is_master():
                return True
        return False
