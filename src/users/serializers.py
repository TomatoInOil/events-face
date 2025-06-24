import rest_framework.serializers
from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework_simplejwt.tokens import RefreshToken

user_model = get_user_model()


@extend_schema_serializer(
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
    component_name="UserCreateResponse",
)
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
