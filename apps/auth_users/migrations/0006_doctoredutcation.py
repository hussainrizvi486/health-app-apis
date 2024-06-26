# Generated by Django 4.2.3 on 2024-05-19 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_users', '0005_alter_user_gender_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorEdutcation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10000)),
                ('start', models.CharField(max_length=10000)),
                ('end', models.CharField(max_length=10000)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_users.doctor')),
            ],
        ),
    ]
