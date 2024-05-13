from rest_framework.permissions import BasePermission


class IsApexAdmin(BasePermission):
    """Allow Access To Organization And Sponsorships"""
        
    def has_permission(self, request, view):
        try:
            return (
                request.user.is_staff or 
                request.user.is_superuser
            )
        except:
            return False