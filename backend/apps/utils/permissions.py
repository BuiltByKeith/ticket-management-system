from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Grants access only to users with the Admin role.
    Used for endpoints that manage system configuration, users, and ticket assignments.
    """

    message = "You must be an administrator to perform this action."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsDeveloper(BasePermission):
    """
    Grants access only to users with the Developer role.
    Used for endpoints that allow developers to view and update their assigned tickets.
    """

    message = "You must be a developer to perform this action."

    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and request.user.is_developer
        )


class IsAdminOrDeveloper(BasePermission):
    """
    Grants access to both Admins and Developers.
    Used for endpoints both roles need to read,
    but with different write capabilities enforced at the view level.
    """

    message = "You must be an authenticated staff member to perform this action."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ("admin", "developer")
        )
