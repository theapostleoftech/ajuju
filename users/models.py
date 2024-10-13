from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from core.models import default_uuid
from users.managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    This is the user model for ajuju
    """
    id = models.CharField(
        default=default_uuid,
        editable=False,
        unique=True,
        max_length=36,
        primary_key=True,
    )
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

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ["email"]

    def get_full_name(self):
        return self.full_name

    def __str__(self):
        return f"{self.email} ({self.full_name})"
