from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.auth_users.models import User


class JWTTokenObtainSerializer(TokenObtainPairSerializer):
    default_error_messages = {"no_active_account": "Invalid credentials"}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        d_user = User.objects.get(email=user.email)
        token["username"] = d_user.username
        token["role"] = d_user.role
        token["phone_number"] = d_user.phone_number
        token["full_name"] = d_user.get_full_name()
        token["email"] = user.email

        return token
