from rest_framework.permissions import BasePermission

class IsNotAuthenticated(BasePermission):
    """
    Permission to only allow unauthenticated users to access the view.
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated
