from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Проверяем, является ли пользователь владельцем объекта
        return obj.owner == request.user


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        # Проверяем, является ли пользователь модератором
        return request.user.groups.filter(name='Moderators').exists()

# Проверяем, что пользователь не является модератором.


class IsNotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name='Moderators').exists()
