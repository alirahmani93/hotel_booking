from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Allows access only to Owners.
    """

    def has_permission(self, request, view) -> bool:
        state: bool = False
        if request.user.is_authenticated:
            try:
                state = True if request.user.owner else False
            except:
                pass
        return state
