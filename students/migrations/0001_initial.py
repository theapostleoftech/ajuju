# Generated by Django 4.2.16 on 2024-10-16 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0006_usermodel_otp_usermodel_otp_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Whizzer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='student', serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Whizzers',
            },
        ),
    ]
