# common/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsAnonymous(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsModerator(BasePermission):
    """
    1. Пользователь должен быть is_staff=True
    2. Может читать (GET), изменять (PUT, PATCH) и удалять (DELETE)
    3. Не может создавать (POST)
    """
    def has_permission(self, request, view):
        # Только модераторы
        if not (request.user and request.user.is_authenticated and request.user.is_staff):
            return False

        # Разрешаем только GET, PUT, PATCH, DELETE
        return request.method in ["GET", "PUT", "PATCH", "DELETE"]

    def has_object_permission(self, request, view, obj):
        # Модератору разрешено всё (кроме POST, который мы выше запретили)
        return True
