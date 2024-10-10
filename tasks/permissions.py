from rest_framework.permissions import BasePermission


class IsCompletedAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.completed == False

    def has_permission(self, request, view):
        return request.user.is_superuser == 1



class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_superuser == True
        return True
