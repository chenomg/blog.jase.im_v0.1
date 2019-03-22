from rest_framework.permissions import BasePermission
from api.models import UserType

class NormalPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.type in (UserType.NORMAL, UserType.ADMIN):
            return True
        else:
            return False
