"""Groups permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from api.groups.models import Membership


class IsGroupAdmin(BasePermission):
    """Allow access to circle admins only."""

    def has_object_permission(self, request, view, obj):
        """Verify user has a membershit in the obj."""
        try:
            Membership.objects.get(
                user=request.user,
                group=obj,
                is_admin=True
            )
        except Membership.DoesNotExist:
            return False
        return True


class IsSelfMember(BasePermission):
    """Allow access only to member owners."""

    def has_permission(self, request, view):
        """Let object permission grant access."""
        obj = view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        """Allow access only if member is owned by the requesting user."""
        return request.user == obj.user