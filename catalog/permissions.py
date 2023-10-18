from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrIfAnonymousReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_anonymous
            )
            or (request.user and request.user.is_staff)
        )
