from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


def success_response(message, data=None, status=status.HTTP_200_OK):
    response = {"message": message}
    if data is not None:
        response["data"] = data
    return Response(
        response,
        status=status,
    )


def internal_server_error_response(message="Something went wrong", error_detail=""):
    return Response(
        {
            "message": message,
            "details": str(error_detail),
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
