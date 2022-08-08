from rest_framework import permissions


class CustomProfileUpdatePermission(permissions.BasePermission):
    """Custom permission class to check that a user can update his own profile only."""
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
