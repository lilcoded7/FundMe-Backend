# django/python imports
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, mixins, generics
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from fund.notifications import EmailSender
from django.shortcuts import render
# local app imports
from accounts.models import User, UserVerificationCode
from .serializers import *
from .middlewares import UserMiddlewares


class CreateUserView(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        user = data.save()
        try:
                
            EmailSender.register_sucess(user)
        except:
            pass
        # TODO: send verification code to user mail
        return Response({"message": "Account created successfully"})


class CreateUserViewSet(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer


class LoginUserView(generics.GenericAPIView, UserMiddlewares):
    serializer_class = LoginUserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        data = data.data

        user = self.get_user_by_email(email=data["email"], password=data["password"])
        if user:
            token = RefreshToken.for_user(user)
            self.get_save_user_device(request, user)
            return Response(
                {
                    "message": "Login successful",
                    # TODO: user active church basic details
                    "user": self.user_serializer(user).data,
                    "tokens": [
                        {
                            "access_token": str(token.access_token),
                            "refresh_token": str(token),
                        }
                    ],
                }
            )
        return Response(
            {
                "message": "Please enter the correct username and password. Note that both fields may be case-sensitive"
            },
            status=404,
        )


class LogoutView(generics.GenericAPIView, UserMiddlewares):
    permission_classes = [AllowAny]
    serializer_class = LogoutSerializer

    def post(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        validated_data = data.data
        try:
            self.logout_user_device(request)
            # Blacklist token
            token = RefreshToken(validated_data["refresh_token"])
            token.blacklist()
            return Response("Successful Logout", 200)
        except Exception as e:
            return Response(str(e), 400)


class PasswordResetRequestCodeView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        validated_data = data.data

        if User.objects.filter(email=validated_data["email"]).exists():
            # Get user
            user = User.objects.get(email=validated_data["email"])
            # Clear all old verification codes if exist
            UserVerificationCode.objects.filter(user=user).delete()

            code = UserVerificationCode.objects.create(user=user)

            # TODO: Send verification code

            return Response(
                {"message": "Password reset code has been sent to your mail"}
            )
        return Response({"message": "User email does not exist"}, 404)


class PasswordResetView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordResetSetPasswordSerializer

    def get(self, request, code):
        verify_code = get_object_or_404(UserVerificationCode, code=code)
        if verify_code and not verify_code.is_expired():
            return Response({"message": "Code valid"})
        return Response({"message": "Invalid code"}, 404)

    def post(self, request, code):
        # Get verification code obj
        verify_code = get_object_or_404(UserVerificationCode, code=code)
        if verify_code and not verify_code.is_expired():
            data = self.serializer_class(data=request.data)
            data.is_valid(raise_exception=True)
            validated_data = data.data

            user = User.objects.get(email=verify_code.user.email)
            user.set_password(validated_data["password"])
            user.save()
            verify_code.delete()
            return Response({"message": "Password reset successful"})
        return Response({"message": "Invalid or expired code provided"}, 400)
    


def home(request):
    return render(request, 'mails/register_sucess.html')