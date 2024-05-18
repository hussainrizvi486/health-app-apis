from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.auth_users.models import User, Doctor
from apps.auth_users.serializers import UserQuerysetSerializer
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

            if user_queryset.role == "Doctor":
                doctor_queryset = Doctor.objects.get(user=user_queryset)
                user_object["about"] = doctor_queryset.about
                user_object["experience"] = doctor_queryset.experience
                user_object["position"] = doctor_queryset.position

            return Response(data=user_object)
        except User.DoesNotExist:
            return Response(data={"message": f"No user found with id {user_id}"})

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
        role = request.GET.get("role")
        for user in userlist_queryset:
            doctor = Doctor.objects.get(user=user)
            data.append(
                {
                    "id": user.id,
                    "name": user.get_full_name(),
                    "position": doctor.position,
                    "experience": doctor.experience,
                    "image": user.image.url if user.image else None,
                }
            )

        if role:
            userlist_queryset = userlist_queryset.filter(role=role)
        serialized_data = UserQuerysetSerializer(userlist_queryset, many=True)
        return Response(data=serialized_data.data)

    def delete_user_profile(self, request):
        try:
            request_body = json.loads(request.data)
        except Exception:
            request_body = request.data

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
            return Response({"message": "User registered successfully"})
        except Exception as e:
            return Response({"message": f"dasf: {str(e)}"}, status=500)

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
        }
        user = User.objects.create_user(**user_dict)
        user.save()
        doctor_profile_object = Doctor.objects.create(
            user=user,
            about=user_data.get("about"),
            experience=user_data.get("experience"),
            position=user_data.get("position"),
        )
        doctor_profile_object.save()
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
