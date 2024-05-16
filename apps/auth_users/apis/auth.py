from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.auth_users.models import User
from apps.auth_users.serializers import UserQuerysetSerializer
import json


class UserCommonAPIS(viewsets.ViewSet):

    def get_user_profile_details(self, request):
        user_id = request.GET.get("id")
        if not user_id:
            return Response(data={"message": "Please provide id in query parameters"})

        try:
            user_queryset = User.objects.get(id=user_id)
            user_object = {
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

    def get_user_profile_list(self, request):
        userlist_queryset = User.objects.all()
        role = request.GET.get("role")
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
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return Response({"message": "Invalid JSON data"}, status=400)
        print(data)
        validated_object = self.validate_user_profile_data(dict(data))
        if not validated_object.get("validated"):
            return Response({"message": validated_object.get("message")}, status=400)

        user_data = validated_object.get("data")
        # try:
        print(user_data)
        user_object = User.objects.create_user(**user_data)
        print(user_object)
        user_object.save()
        return Response({"message": "User registered successfully"})
        # except Exception as e:
        #     return Response({"message": f'dasf: {str(e)}'}, status=500)

    def validate_user_profile_data(self, data: dict) -> dict:
        data["role"] = "Admin"
        mandatory_fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "gender",
            "date_of_birth",
            # "image",
            "address",
            "password",
        ]

        for field in mandatory_fields:
            if field not in data:
                return {"message": f"{field} is missing!", "validated": False}

        return {"data": data, "validated": True}
