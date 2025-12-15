from rest_framework import permissions


class IsAdminUserForWriteOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        return user.is_staff and user.is_authenticated
