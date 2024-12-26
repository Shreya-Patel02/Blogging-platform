from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Owner'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Admin'

class IsMember(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Member'
