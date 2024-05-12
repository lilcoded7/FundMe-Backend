from django.contrib.auth import get_user_model

from accounts.models import LoggedInUserDevices
from .utils import get_user_ip_address
from .serializers import UserSerializer

User = get_user_model()


class UserMiddlewares:
    user_serializer = UserSerializer

    def get_user_by_email(self, email, password):
        # Check against email and password
        try:
            user = User.objects.get(email=email)
            passcheck = user.check_password(password)
            return user if passcheck else False
        except User.DoesNotExist:
            return False

    def get_save_user_device(self, request, user):
        LoggedInUserDevices.objects.create(
            user=user,
            ip_address=get_user_ip_address(request),
            browser=request.user_agent.browser.family,
            os=request.user_agent.os,
        )

    def logout_user_device(self, request):
        LoggedInUserDevices.objects.filter(
            ip_address=get_user_ip_address(request), is_active=True
        ).update(is_active=False)