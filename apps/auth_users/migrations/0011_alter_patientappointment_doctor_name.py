# Generated by Django 4.2.3 on 2024-05-19 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_users', '0010_patientappointment_doctor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientappointment',
            name='doctor_name',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
