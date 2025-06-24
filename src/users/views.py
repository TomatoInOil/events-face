import rest_framework.generics
from django.contrib.auth import get_user_model

from src.users.serializers import UserCreateSerializer

user_model = get_user_model()


class UserCreate(rest_framework.generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = user_model.objects.all()


class TokenBlacklistView(rest_framework.generics.GenericAPIView):
    pass
