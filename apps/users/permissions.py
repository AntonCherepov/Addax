from rest_framework.permissions import BasePermission

from core.decorators import get_user_decorator


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsConfirmed(BasePermission):
    """
    Allows access only to confirmed users.
    """
    @get_user_decorator
    def has_permission(self, request, user, view):
        return user.is_confirmed() if user else False


class IsNotBanned(BasePermission):
    """
    Allows access only to not banned users.
    """
    @get_user_decorator
    def has_permission(self, request, user, view):
        # user can't be banned if he is not exist
        return not user.is_banned() if user is not None else True


class IsBalancePositive(BasePermission):
    """
    Allows access only to for
    users with positive balance.
    """
    @get_user_decorator
    def has_permission(self, request, user, view):
        if user.is_master():
            return user.balance.is_positive()
        return True


class MasterReadOnly(BasePermission):
    """
    Allows read only access for masters.
    """

    @get_user_decorator
    def has_permission(self, request, user, view):
        return True if request.method in SAFE_METHODS or not user.is_master() \
                    else False


class IsMaster(BasePermission):
    """
    Allows access only for masters.
    """

    @get_user_decorator
    def has_permission(self, request, user, view):
        return user.is_master()


class IsClient(BasePermission):
    """
    Allows access only for clients.
    """
    @get_user_decorator
    def has_permission(self, request, user, view):
        return user.is_client()
