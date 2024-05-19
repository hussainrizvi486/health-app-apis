from rest_framework import viewsets, status
from rest_framework.response import Response
from apps.auth_users.models import *
from apps.auth_users.serializers import PatientAppointmentSerializer
from ..utils import load_request_body


class AppointmentApis(viewsets.ViewSet):
    def current_patient_appointments(self, request):
        try:
            patient = Patient.objects.get(user=request.user)
            print(patient.get_appointments())
            return Response(data=patient.get_appointments())
        except Exception as e:
            return Response(data={"message": str(e)})

    def get_all_pending_appointments(self, request):
        try:
            appointments = PatientAppointment.objects.filter(status="Pending")
            serialized_data = PatientAppointmentSerializer(appointments, many=True)
            return Response(data=serialized_data.data)
        except Exception as e:
            return Response(data={"message": str(e)})

    def create_appointment(self, request):
        data = load_request_body(request.data)

        patient_id = data.get("patient_id")
        doctor_id = data.get("doctor_id")
        doctor_name = data.get("doctor_name")
        appointment_date = data.get("appointment_date")
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        d_status = data.get("status", "Pending")
        # Validate the required fields
        if not (
            patient_id and doctor_id and appointment_date and start_time and end_time
        ):
            return Response(
                {"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            patient = Patient.objects.get(id=patient_id)
            doctor = Doctor.objects.get(id=doctor_id)
            appointment_obj = PatientAppointment.objects.create(
                patient=patient,
                doctor=doctor,
                doctor_name=doctor_name,
                appointment_date=appointment_date,
                start_time=start_time,
                end_time=end_time,
                status=d_status,
            )
            appointment_obj.save()
            return Response(
                {"message": "Appointment created successfully!"},
                status=status.HTTP_201_CREATED,
            )

        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Doctor.DoesNotExist:
            return Response(
                {"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
