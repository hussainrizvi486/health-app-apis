from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.auth_users.serializers import JWTTokenObtainSerializer
from apps.auth_users.apis import UserCommonAPIS, RegisterProfilesAPIS


class AuthTokenObtainPairView(TokenObtainPairView):
    serializer_class = JWTTokenObtainSerializer


urlpatterns = [
    path("api/token/", AuthTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/user/admin/login",
        AuthTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/user/doctor/login",
        AuthTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/user/patient/login",
        AuthTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # USER APIS
    path(
        "api/manage/profile/list",
        UserCommonAPIS.as_view({"get": "get_user_profile_list"}),
    ),
    path(
        "api/user/profile/delete",
        UserCommonAPIS.as_view({"post": "delete_user_profile"}),
    ),
    # Registration apis
    path(
        "api/register/user/admin",
        RegisterProfilesAPIS.as_view({"post": "register_admin_profile"}),
    ),
    path(
        "api/register/user/doctor",
        RegisterProfilesAPIS.as_view({"post": "register_doctor_profile"}),
    ),
    # --------------------------------------------
    path(
        "api/doctor/list",
        UserCommonAPIS.as_view({"get": "get_doctor_profile_list"}),
    ),
    path(
        "api/admin/list",
        UserCommonAPIS.as_view({"get": "get_admin_profile_list"}),
    ),
    path(
        "api/patient/list",
        UserCommonAPIS.as_view({"get": "get_patient_profile_list"}),
    ),
    path(
        "api/profile/detail",
        UserCommonAPIS.as_view({"get": "get_user_profile_details"}),
    ),
    path(
        "api/appointments/pending",
        UserCommonAPIS.as_view({"get": "get_all_pending_appointments"}),
    ),
    path(
        "api/patient/my-appointments",
        UserCommonAPIS.as_view({"get": "current_patient_appointments"}),
    ),
]
