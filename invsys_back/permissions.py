from requests import request
from rest_framework import permissions

class AdminLevelOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.user_level)
        if request.user.user_level.group_level == 1:
            return True
        else:
            return False

class CurrentUserOrAdminLevel(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.user_level)
        if request.user.user_level.group_level == 1:
            return True
        else:
            return False
            
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.user_level.group_level == 1 or obj.pk == user.pk
