from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from apps.auth_users.serializers import JWTTokenObtainSerializer
from apps.auth_users.apis import (
    UserCommonAPIS,
    RegisterProfilesAPIS,
    AppointmentApis,
    UpdateProfilesAPIS,
)


class AuthTokenObtainPairView(TokenObtainPairView):
    serializer_class = JWTTokenObtainSerializer


urlpatterns = [
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
    # USER APIS
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
    path(
        "api/register/user/patient",
        RegisterProfilesAPIS.as_view({"post": "register_patient_profile"}),
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
        "api/admin/profile/detail",
        UserCommonAPIS.as_view({"get": "get_user_profile_details"}),
    ),
    path(
        "api/doctor/profile/detail",
        UserCommonAPIS.as_view({"get": "get_doctor_profile_detail"}),
    ),
    path(
        "api/patient/profile/detail",
        UserCommonAPIS.as_view({"get": "get_patient_profile_detail"}),
    ),
    path(
        "api/appointments/pending",
        AppointmentApis.as_view({"get": "get_all_pending_appointments"}),
    ),
    path(
        "api/patient/my-appointments",
        AppointmentApis.as_view({"get": "current_patient_appointments"}),
    ),
    path(
        "api/appointments/all",
        AppointmentApis.as_view({"get": "get_all_appointments"}),
    ),
    path(
        "api/appointments/all/scheduled",
        AppointmentApis.as_view({"get": "get_all_appointments_scheduled"}),
    ),
    path(
        "api/appointments/all/pending",
        AppointmentApis.as_view({"get": "get_all_appointments_pending"}),
    ),
    # 
    path(
        "api/doctor/appointments/all",
        AppointmentApis.as_view({"get": "get_all_doctor_appointments"}),
    ),
    path(
        "api/doctor/appointments/scheduled",
        AppointmentApis.as_view({"get": "get_scheduled_doctor_appointments"}),
    ),
    path(
        "api/doctor/appointments/cancel",
        AppointmentApis.as_view({"get": "get_cancel_doctor_appointments"}),
    ),
    # 
    path(
        "api/appointments/create",
        AppointmentApis.as_view({"post": "create_appointment"}),
    ),
    path(
        "api/appointments/approve",
        AppointmentApis.as_view({"post": "approve_appointment"}),
    ),
    path(
        "api/appointments/cancel",
        AppointmentApis.as_view({"post": "cancel_appointment"}),
    ),
    path(
        "api/appointments/complete",
        AppointmentApis.as_view({"post": "complete_appointment"}),
    ),
    path(
        "api/user/admin/update",
        UpdateProfilesAPIS.as_view({"post": "update_admin_profile"}),
    ),
    path(
        "api/user/patient/update",
        UpdateProfilesAPIS.as_view({"post": "update_patient_profile"}),
    ),
    path(
        "api/user/doctor/update",
        UpdateProfilesAPIS.as_view({"post": "update_doctor_profile"}),
    ),
]
