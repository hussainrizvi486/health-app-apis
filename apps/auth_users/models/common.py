from django.db import models
from .user import User
from django.utils import timezone
from datetime import timedelta, datetime


class Doctor(models.Model):
    experience = models.CharField(max_length=50, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=50, null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username or self.user.email or ""


class DoctorEducation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    name = models.CharField(max_length=10000)
    start = models.CharField(max_length=10000)
    end = models.CharField(max_length=10000)


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username or self.user.email or ""

    def get_appointments(self):
        appointments = self.patientappointment_set.all()
        appointments_list = []
        for appointment in appointments:
            appointment_dict = {
                "patient": self.user.username,
                "doctor_id": appointment.doctor.id,
                "doctor_name": appointment.doctor_name,
                "appointment_date": appointment.appointment_date.isoformat(),
                "start_time": appointment.start_time.isoformat(),
                "end_time": appointment.end_time.isoformat(),
                "status": appointment.status,
            }
            appointments_list.append(appointment_dict)
        return appointments_list


class PatientAppointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    doctor_name = models.CharField(max_length=1000, null=True)
    appointment_date = models.DateField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Scheduled", "Scheduled"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Scheduled",
    )

    def save(self, *args, **kwargs):
        self.doctor_name = self.doctor.user.username or self.doctor.user.email
        if not self.start_time:
            self.start_time = timezone.make_aware(
                datetime.combine(self.appointment_date, datetime.min.time())
            )
        if not self.end_time:
            self.end_time = self.start_time + timedelta(hours=1)
        super(PatientAppointment, self).save(*args, **kwargs)
