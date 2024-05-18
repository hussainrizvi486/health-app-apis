from rest_framework.serializers import ModelSerializer
from apps.auth_users.models import User


class UserQuerysetSerializer(ModelSerializer):
    class Meta:
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "role",
            "gender",
            "date_of_birth",
            "image",
            "address",
            "is_superuser",
        ]

        model = User
