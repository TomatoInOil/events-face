from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

from src.core.redis_client import get_redis_client


class RedisBlacklistJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        token = super().get_validated_token(raw_token)
        jti = str(token["jti"])
        redis_client = get_redis_client()
        if redis_client.get(f"bl_{jti}"):
            raise InvalidToken("Token is blacklisted")
        return token


class RedisBlacklistJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "src.users.authentication.RedisBlacklistJWTAuthentication"
    name = "JWTAuthentication"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
