from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == "Admin"


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role.name == "Author" and obj.user == request.user
