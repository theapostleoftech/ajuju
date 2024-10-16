"""
This is the model for the students
"""
from django.db import models


# Create your models here.
class Whizzer(models.Model):
    """
    This is the teacher model
    """
    user = models.OneToOneField(
        'users.UserModel',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='student'
    )

    class Meta:
        verbose_name_plural = "Whizzers"

    def __str__(self):
        return f"{self.user.email} {self.user.full_name}"

    pass
