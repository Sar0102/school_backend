from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView as BaseTokenObtainPairView,
)
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView

from core.models import User
from core.serializers import LoginPayloadSerializer


class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = LoginPayloadSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(
            username=serializer.validated_data["username"]
        ).first()
        if user is None:
            raise serializers.ValidationError(
                {"message": "User doesn't exist with this email"}
            )
        else:
            if not user.check_password(serializer.validated_data["password"]):
                raise serializers.ValidationError({"message": "Password is incorrect"})
            if not user.is_active:
                raise serializers.ValidationError(
                    {"message": "Your profile is not activated"}
                )
        refresh_token = RefreshToken.for_user(user)
        refresh_token["role"] = user.role
        return Response(
            {
                "refresh": str(refresh_token),
                "access": str(refresh_token.access_token),
                "role": user.role,
            }
        )


class TokenRefreshView(BaseTokenRefreshView): ...
