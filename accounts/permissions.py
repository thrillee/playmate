from requests.api import request
from rest_framework import permissions

from .models import PlayMateUser as User


class IsUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            user = User.objects.get(phone_number=request.user.phone_number)
            if request.user == user:
                return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.user == request.user:
            return True
        return False


class UserInThread(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.user.IsAuthenticated:
            if obj.user == obj.thread.first or obj.user == obj.thread.second:
                return True
        return False
