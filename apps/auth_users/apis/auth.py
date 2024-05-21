from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.auth_users.models import (
    User,
    Doctor,
    DoctorEducation,
    Patient,
    PatientAppointment,
)
from apps.auth_users.serializers import (
    UserQuerysetSerializer,
    PatientAppointmentSerializer,
)
from ..utils import load_request_body
import json


class UserCommonAPIS(viewsets.ViewSet):
    def get_user_profile_details(self, request):
        user_id = request.GET.get("id")
        if not user_id:
            return Response(data={"message": "Please provide id in query parameters"})

        try:
            user_queryset = User.objects.get(id=user_id)
            user_object = {
                "user_id": user_queryset.id,
                "email": user_queryset.email,
                "full_name": user_queryset.get_full_name(),
                "gender": user_queryset.gender,
                "role": user_queryset.role,
                "date_of_birth": (
                    user_queryset.date_of_birth.strftime("%m-%d-%Y")
                    if user_queryset.date_of_birth
                    else None
                ),
                "phone_number": user_queryset.phone_number,
            }

            return Response(data=user_object)
        except User.DoesNotExist:
            return Response(data={"message": f"No user found with id {user_id}"})

    def get_patient_profile_detail(self, request):
        user_id = request.GET.get("id")
        if not user_id:
            return Response(data={"message": "Please provide id in query parameters"})

        try:
            user_queryset = User.objects.get(id=user_id)

            patient = Patient.objects.get(user=user_queryset)

            user_object = {
                "user_id": user_queryset.id,
                "email": user_queryset.email,
                "full_name": user_queryset.get_full_name(),
                "gender": user_queryset.gender,
                "role": user_queryset.role,
                "date_of_birth": (
                    user_queryset.date_of_birth.strftime("%m-%d-%Y")
                    if user_queryset.date_of_birth
                    else None
                ),
                "phone_number": user_queryset.phone_number,
                "appointments": patient.get_appointments(),
            }
            return Response(data=user_object)
        except User.DoesNotExist:
            return Response(data={"message": f"No user found with id {user_id}"})

    def get_doctor_profile_detail(self, request):
        user_id = request.GET.get("id")
        if not user_id:
            return Response(data={"message": "Please provide id in query parameters"})

        try:
            user_queryset = User.objects.get(id=user_id)
            user_object = {
                "user_id": user_queryset.id,
                "email": user_queryset.email,
                "full_name": user_queryset.get_full_name(),
                "gender": user_queryset.gender,
                "role": user_queryset.role,
                "date_of_birth": (
                    user_queryset.date_of_birth.strftime("%m-%d-%Y")
                    if user_queryset.date_of_birth
                    else None
                ),
                "phone_number": user_queryset.phone_number,
            }

            doctor_queryset = Doctor.objects.get(user=user_queryset)
            user_object["about"] = doctor_queryset.about
            user_object["experience"] = doctor_queryset.experience
            user_object["position"] = doctor_queryset.position
            user_object["education"] = DoctorEducation.objects.filter(
                doctor=doctor_queryset
            ).values("name", "start", "end")

            return Response(data=user_object)
        except User.DoesNotExist:
            return Response(data={"message": f"No doctor found with id {user_id}"})

    def get_user_profile_list(self, request):
        userlist_queryset = User.objects.all()
        role = request.GET.get("role")
        if role:
            userlist_queryset = userlist_queryset.filter(role=role)
        serialized_data = UserQuerysetSerializer(userlist_queryset, many=True)
        return Response(data=serialized_data.data)

    def get_doctor_profile_list(self, request):
        data = []
        userlist_queryset = User.objects.filter(role="Doctor")
        for user in userlist_queryset:
            doctor = Doctor.objects.get(user=user)
            data.append(
                {
                    "id": user.id,
                    "name": user.get_full_name(),
                    "position": doctor.position,
                    "experience": doctor.experience,
                    "image": user.image.url if user.image else None,
                    "education": DoctorEducation.objects.filter(doctor=doctor).values(
                        "name", "start", "end"
                    ),
                }
            )
        return Response(data=data)

    def get_admin_profile_list(self, request):
        userlist_queryset = User.objects.filter(role="Admin")
        serialized_data = UserQuerysetSerializer(userlist_queryset, many=True)
        return Response(data=serialized_data.data)

    def get_patient_profile_list(self, request):
        userlist_queryset = User.objects.filter(role="Patient")
        serialized_data = UserQuerysetSerializer(userlist_queryset, many=True)
        return Response(data=serialized_data.data)

    def delete_user_profile(self, request):
        request_body = load_request_body(request.data)
        user_id = request_body.get("id")
        if not user_id:
            return Response(data={"message": "Please provide id in query parameters"})

        try:
            User.objects.get(id=user_id).delete()
            return Response(data={"message": "User profile deleted successfully"})
        except User.DoesNotExist:
            return Response(data={"message": f"No user found with id {user_id}"})


class RegisterProfilesAPIS(viewsets.ViewSet):
    def register_admin_profile(self, request):
        data = request.data
        data = load_request_body(data)
        validated_object = self.validate_user_profile_data(dict(data), "Admin")
        if not validated_object.get("validated"):
            return Response({"message": validated_object.get("message")}, status=400)

        user_data = validated_object.get("data")
        try:
            user_object = User.objects.create_superuser(**user_data)
            user_object.save()
            return Response({"message": "User registered successfully!"})
        except Exception as e:
            return Response({"message": str(e)}, status=500)

    def register_patient_profile(self, request):
        data = request.data
        data = load_request_body(data)
        validated_object = self.validate_user_profile_data(dict(data), "Patient")
        if not validated_object.get("validated"):
            return Response({"message": validated_object.get("message")}, status=400)

        user_data: dict = validated_object.get("data")
        user = User.objects.create_user(**user_data)
        user.save()

        patient = Patient.objects.create(user=user)
        patient.save()

        return Response({"message": "Patient profile created successfully"})
        ...

    def register_doctor_profile(self, request):
        data = request.data
        data = load_request_body(data)
        validated_object = self.validate_user_profile_data(dict(data), "Doctor")
        if not validated_object.get("validated"):
            return Response({"message": validated_object.get("message")}, status=400)

        user_data: dict = validated_object.get("data")
        user_dict = {
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "email": user_data.get("email"),
            "phone_number": user_data.get("phone_number"),
            "gender": user_data.get("gender"),
            "date_of_birth": user_data.get("date_of_birth"),
            "address": user_data.get("address"),
            "password": user_data.get("password"),
            "role": user_data.get("role"),
        }

        education_data = user_data.get("education")

        user = User.objects.create_user(**user_dict)
        user.save()
        doctor_profile_object = Doctor.objects.create(
            user=user,
            about=user_data.get("about"),
            experience=user_data.get("experience"),
            position=user_data.get("position"),
        )

        doctor_profile_object.save()
        if education_data:
            for row in education_data:
                edu_object = DoctorEducation.objects.create(
                    doctor=doctor_profile_object,
                    name=row.get("name"),
                    start=row.get("start"),
                    end=row.get("end"),
                )
                edu_object.save()

        return Response({"message": "Doctor profile created successfully"})

    def validate_user_profile_data(self, data: dict, role="") -> dict:
        data["role"] = role
        mandatory_fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "gender",
            "date_of_birth",
            "address",
            "password",
            # "image",
        ]

        for field in mandatory_fields:
            if field not in data:
                return {"message": f"{field} is missing!", "validated": False}
        return {"data": data, "validated": True}


class UpdateProfilesAPIS(viewsets.ViewSet):
    def update_admin_profile(self, request):
        data = request.data
        data = load_request_body(data)
        validated_object = self.validate_user_profile_data(dict(data))
        if not validated_object.get("validated"):
            return Response({"message": validated_object.get("message")}, status=400)

        user_data = validated_object.get("data")

        id = user_data.get("id")
        del user_data["id"]
        User.objects.filter(id=id).update(**user_data)
        return Response({"message": "Admin updated successfully!"})

    def update_patient_profile(self, request):
        data = request.data
        data = load_request_body(data)
        validated_object = self.validate_user_profile_data(dict(data))
        if not validated_object.get("validated"):
            return Response({"message": validated_object.get("message")}, status=400)

        user_data = validated_object.get("data")
        id = user_data.get("id")
        del user_data["id"]
        User.objects.filter(id=id).update(**user_data)
        return Response({"message": "Patient updated successfully!"})

    def update_doctor_profile(self, request):
        data = request.data
        data = load_request_body(data)
        validated_object = self.validate_user_profile_data(dict(data))
        if not validated_object.get("validated"):
            return Response({"message": validated_object.get("message")}, status=400)

        user_data: dict = validated_object.get("data")
        user_dict = {
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "email": user_data.get("email"),
            "phone_number": user_data.get("phone_number"),
            "gender": user_data.get("gender"),
            "date_of_birth": user_data.get("date_of_birth"),
            "address": user_data.get("address"),
        }

        education_data = user_data.get("education")
        id = user_data.get("id")
        User.objects.filter(id=id).update(**user_dict)
        user = User.objects.get(id=id)
        Doctor.objects.filter(user=user).update(
            user=user,
            about=user_data.get("about"),
            experience=user_data.get("experience"),
            position=user_data.get("position"),
        )

        doctor_profile_object = Doctor.objects.get(user=user)
        DoctorEducation.objects.filter(doctor=doctor_profile_object).delete()
        if education_data:
            for row in education_data:
                edu_object = DoctorEducation.objects.create(
                    doctor=doctor_profile_object,
                    name=row.get("name"),
                    start=row.get("start"),
                    end=row.get("end"),
                )
                edu_object.save()

        return Response({"message": "Doctor profile updated successfully"})

    def validate_user_profile_data(self, data: dict) -> dict:
        mandatory_fields = [
            "first_name",
            "last_name",
            "phone_number",
            "gender",
            "date_of_birth",
            # "address",
        ]

        for field in mandatory_fields:
            if field not in data:
                return {"message": f"{field} is missing!", "validated": False}
        return {"data": data, "validated": True}
