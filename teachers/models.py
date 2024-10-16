from django.db import models


# Create your models here.
class Creator(models.Model):
    """
    This is the teacher model
    """
    user = models.OneToOneField(
        'users.UserModel',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='teacher'
    )

    class Meta:
        verbose_name_plural = "Creators"

    def __str__(self):
        return f"{self.user.email} ({self.user.full_name})"

    pass
