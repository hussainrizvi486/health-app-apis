from rest_framework.serializers import ModelSerializer
from apps.auth_users.models import User, PatientAppointment, Patient, Doctor


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


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class PatientSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ["user"]


class DoctorSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ["user", "experience", "position", "about"]


class PatientAppointmentSerializer(ModelSerializer):
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = PatientAppointment
        fields = [
            "patient",
            "doctor",
            "doctor_name",
            "appointment_date",
            "start_time",
            "end_time",
            "status",
        ]
