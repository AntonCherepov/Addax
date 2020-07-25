from django.core.exceptions import SuspiciousOperation


class BadRequestError(SuspiciousOperation):
    """The request is incorrect"""
    pass


class RequestUserError(SuspiciousOperation):
    """The request.user error"""
    pass
