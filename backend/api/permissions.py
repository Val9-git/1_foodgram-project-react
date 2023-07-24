from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Только автор или чтение."""
    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Только Админ или чтение."""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS or request.user.is_staff
        )
