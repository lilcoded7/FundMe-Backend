from django.urls import path, include
from .views import *

app_name = "accounts"

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="accounts_register"),
    path("login/", LoginUserView.as_view(), name="accounts_login"),
    path("logout/", LogoutView.as_view(), name="accounts_logout"),
    path(
        "reset/<int:code>/", PasswordResetView.as_view(), name="accounts_password_reset"
    ),
    path(
        "reset-request",
        PasswordResetRequestCodeView.as_view(),
        name="accounts_password_request_code",
    ),
]