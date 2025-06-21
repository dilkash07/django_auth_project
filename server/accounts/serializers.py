from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .mail.template.otp_verification_template import otp_template
from .mail.template.reset_message_template import reset_emai_message_template
import random
from accounts.models import OTP


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "tc",
            "password",
            "confirm_password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        email = attrs.get("email")

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match"
            )
        return attrs

    def create(self, validated_data):
        try:
            validated_data.pop("confirm_password")
            return User.objects.create_user(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(
                {"error": "User creation failed", "details": str(e)}
            )

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "created_at": instance.created_at,
        }


class SendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User already registered")
        return value

    def create(self, validated_data):
        email = validated_data["email"]
        code = str(random.randint(100000, 999999))

        # save otp in DB
        OTP.objects.create(email=email, code=code)

        send_mail(
            subject="Verification Email",
            message="",
            from_email=None,
            recipient_list=[email],
            html_message=otp_template(code),
            fail_silently=False,
        )
        return email


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get("email", "").strip().lower()
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("Account is inactive")

        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "tc", "created_at"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=255, required=True, style={"input_type": "password"}, write_only=True
    )
    new_password = serializers.CharField(
        max_length=255, required=True, style={"input_type": "password"}, write_only=True
    )
    confirm_new_password = serializers.CharField(
        max_length=255, required=True, style={"input_type": "password"}, write_only=True
    )

    def validate(self, attrs):
        user = self.context.get("user")
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        confirm_new_password = attrs.get("confirm_new_password")

        if not user.check_password(old_password):
            raise serializers.ValidationError("Old Password is incorrect")

        if new_password != confirm_new_password:
            raise serializers.ValidationError("New Password doesn't match")
        return attrs

    def save(self, **kwargs):
        user = self.context.get("user")
        new_password = self.validated_data.get("new_password")
        user.set_password(new_password)
        user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User doesn't exist with this email")
        return value

    def save(self, **kwargs):
        email = self.validated_data["email"]
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_url = f"http://127.0.0.1:8000/api/user/reset-password/{uid}/{token}/"

        # print(uid, token, reset_url)

        send_mail(
            subject="Reset Your Password",
            message="Use the link below to reset your password.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=reset_emai_message_template(user, reset_url),
            fail_silently=False,
        )


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=6, write_only=True)
    confirm_new_password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_new_password"]:
            raise serializers.ValidationError("Password doesn't match")
        return attrs

    def save(self, uid, token):
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError("Invalid UID")

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("Invalid or expired token")

        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
