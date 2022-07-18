from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Permission class for owner"""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author_user_id == request.user:
            return True

        return False

    # TODO : make it works !