import rest_framework.generics
from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework_simplejwt.views import TokenRefreshView

from src.users.serializers import (
    RedisBlacklistTokenRefreshSerializer,
    TokenBlacklistSerializer,
    UserCreateSerializer,
)

user_model = get_user_model()


@extend_schema(
    responses=UserCreateSerializer,
    examples=[
        OpenApiExample(
            "User created",
            value={
                "message": "User created successfully",
                "access": "access_token_string",
                "refresh": "refresh_token_string",
            },
            response_only=True,
            status_codes=["201"],
        )
    ],
)
class UserCreate(rest_framework.generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = user_model.objects.all()


@extend_schema(
    responses={
        204: None,
    }
)
class TokenBlacklistView(rest_framework.generics.GenericAPIView):
    serializer_class = TokenBlacklistSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return rest_framework.response.Response(
            status=rest_framework.status.HTTP_204_NO_CONTENT
        )


class RedisBlacklistTokenRefreshView(TokenRefreshView):
    serializer_class = RedisBlacklistTokenRefreshSerializer
