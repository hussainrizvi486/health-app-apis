from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.auth_users.serializers import JWTTokenObtainSerializer
from apps.auth_users.apis import UserCommonAPIS,RegisterProfilesAPIS


class AuthTokenObtainPairView(TokenObtainPairView):
    serializer_class = JWTTokenObtainSerializer


urlpatterns = [
    path("api/token/", AuthTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # USER APIS
    path(
        "api/manage/profile/detail",
        UserCommonAPIS.as_view({"get": "get_user_profile_details"}),
    ),
    path(
        "api/manage/profile/list",
        UserCommonAPIS.as_view({"get": "get_user_profile_list"}),
    ),
    path(
        "api/manage/profile/delete",
        UserCommonAPIS.as_view({"post": "delete_user_profile"}),
    ),
    path(
        "api/register/user/admin",
        RegisterProfilesAPIS.as_view({"post": "register_admin_profile"}),
    ),
]
