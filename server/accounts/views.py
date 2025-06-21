from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import (
    UserRegistrationSerializer,
    SendOtpSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from .renderers import UserRenderer
from .utils import get_tokens_for_user, success_response, internal_server_error_response
from rest_framework.permissions import IsAuthenticated


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                return success_response(
                    "User registered Successfully",
                    serializer.data,
                    status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return internal_server_error_response(
                "Something went wrong while registering user", e
            )


class SendOtpView(APIView):
    def post(self, request):
        try:
            serializer = SendOtpSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return success_response(
                    "OTP sent successfully", status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return internal_server_error_response(
                "Something went wrong while sending OTP", e
            )


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        try:
            serializer = UserLoginSerializer(data=request.data)

            if serializer.is_valid():
                user = serializer.validated_data["user"]
                token = get_tokens_for_user(user)
                data = {
                    "token": token,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                }

                return success_response(
                    "User logged in successfully", data, status.HTTP_200_OK
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return internal_server_error_response(
                "Something went wrong while login user", e
            )


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            user = request.user
            serializer = UserProfileSerializer(user)
            return success_response(
                "User profile fetched successfully", serializer.data, status.HTTP_200_OK
            )

        except Exception as e:
            return internal_server_error_response(
                "Something went wrong while fetching user profile", e
            )


class ChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def patch(self, request, format=None):
        try:
            user = request.user
            serializer = ChangePasswordSerializer(
                data=request.data, context={"user": user}
            )

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return success_response("Password changed successfully")
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return internal_server_error_response(
                "Something went wrong while changing password", e
            )


class ForgotPasswordView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        try:
            serializer = ForgotPasswordSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return success_response(
                    "Reset link sent successfully", status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return internal_server_error_response(
                "Something went wrong while sending email", e
            )


class ResetPasswordView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(uid, token)
                return success_response(
                    "Password reset successfully",
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return internal_server_error_response(
                "Something went wrong while resetting password", e
            )
