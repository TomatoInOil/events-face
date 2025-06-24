from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from src.users.views import (
    RedisBlacklistTokenRefreshView,
    TokenBlacklistView,
    UserCreate,
)

app_name = "users"

urlpatterns = [
    path("auth/register/", UserCreate.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "auth/token/refresh/",
        RedisBlacklistTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("auth/logout/", TokenBlacklistView.as_view(), name="logout"),
]
