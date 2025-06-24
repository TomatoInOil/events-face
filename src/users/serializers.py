import rest_framework.serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from src.core.redis_client import get_redis_client

user_model = get_user_model()


class UserCreateSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = user_model
        fields = ("username", "password")
        extra_kwargs = {
            "username": {"write_only": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = user_model.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            "message": "User created successfully",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class TokenBlacklistSerializer(rest_framework.serializers.Serializer):
    refresh = rest_framework.serializers.CharField()

    def validate(self, attrs):
        try:
            refresh = RefreshToken(attrs["refresh"])
        except TokenError as e:
            raise InvalidToken(e.args[0])

        jti = str(refresh["jti"])
        exp = int(refresh["exp"])
        now = int(refresh.current_time.timestamp())
        ttl = exp - now

        redis_client = get_redis_client()
        redis_client.setex(f"bl_{jti}", ttl, "blacklisted")
        return attrs

    def create(self, validated_data):
        return validated_data


class RedisBlacklistTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = attrs["refresh"]
        try:
            refresh_token = self.token_class(refresh)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        jti = str(refresh_token["jti"])
        redis_client = get_redis_client()
        if redis_client.get(f"bl_{jti}"):
            raise InvalidToken("Token is blacklisted")

        return super().validate(attrs)
