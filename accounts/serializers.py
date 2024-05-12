from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["id", "password", "is_admin", "is_staff", "is_superuser"]


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "profile",
            "username",
            "full_name",
            "email",
            "phone_number",
            "user_status",
        ]

    def create(self, validated_data):
        password = validated_data.get("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255)


class PasswordResetSetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()

    def validate_password(self, password):
        # check for small letters
        if not any(char.islower() for char in password):
            raise serializers.ValidationError(
                {"message": "Weak password, Must contain at least one small letter"}
            )

        # check for capital letters
        if not any(char.isupper() for char in password):
            raise serializers.ValidationError(
                {"message": "Weak password, Must contain at least one capital letter"}
            )

        # check for numbers
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError(
                {"message": "Weak password, Must contain at least one number"}
            )

        # check for characters
        if not any(char.isascii() for char in password):
            raise serializers.ValidationError(
                {"message": "Weak password, Must contain at least one character"}
            )

        return password


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField()