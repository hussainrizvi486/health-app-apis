from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, DoctorEducation, Patient, PatientAppointment


class DoctorEducationInline(admin.TabularInline):
    model = DoctorEducation


class DoctorAdmin(admin.ModelAdmin):
    inlines = [DoctorEducationInline]


admin.site.register(Doctor, DoctorAdmin)


class PatientAppointmentInline(admin.TabularInline):
    model = PatientAppointment


class PatientAdmin(admin.ModelAdmin):
    inlines = [PatientAppointmentInline]


admin.site.register(Patient, PatientAdmin)
admin.site.register(PatientAppointment)


@admin.register(User)
class UserAdminView(UserAdmin):
    list_display = ["email", "username", "phone_number"]
    list_filter = ["date_joined"]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            ("Personal info"),
            {
                "fields": (
                    "image",
                    "first_name",
                    "last_name",
                    "gender",
                    "email",
                    "phone_number",
                    "role",
                    "address",
                    # "date_of_birth",
                )
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "phone_number",
                    "email",
                    "role",
                    "address",
                    # "date_of_birth",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                )
            },
        ),
        (
            "Password",
            {
                "fields": (
                    "password1",
                    "password2",
                )
            },
        ),
    )
