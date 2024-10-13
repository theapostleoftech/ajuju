from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=255,
        unique=True,
        db_index=True
    )
    email = models.EmailField(
        verbose_name='Email address',
        unique=True,
        db_index=True,
    )
    full_name = models.CharField(
        max_length=255,
        blank=True,
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    def get_full_name(self):
        return self.full_name

    def __str__(self):
        return f"{self.email} ({self.full_name})"
