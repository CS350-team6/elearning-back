# Standard Library imports

# Core Django imports

# Third-party imports
from rest_framework import permissions

# App imports

class AccountCreation(permissions.BasePermission):
    """   A user should be able to create an account without being authenticated, but only the
          owner of an account should be able to access that account's data in a GET method.
    """

    def has_permission(self, request, view):
        if (request.method == "POST") or request.user.is_authenticated:
            return True
        return False