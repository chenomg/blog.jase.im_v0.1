from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import UserType

class NormalUserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.type in (UserType.NORMAL, UserType.ADMIN):
            return True
        else:
            return False

class HasTokenOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user
        )

