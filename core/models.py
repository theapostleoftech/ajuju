from uuid import uuid4

from django.db import models

# Create your models here.
def default_uuid():
    """
    Generate a default UUID for model instances.

    Returns:
        str: A string representation of a UUID4, which is a randomly generated UUID.
    """
    return str(uuid4())

class BaseModel(models.Model):
    """
    This is the base model for all models in the application
    """
    id = models.CharField(
        default=default_uuid,
        editable=False,
        unique=True,
        primary_key=True,
        max_length=36,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date Created'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Date Modified'
    )

    class Meta:
        abstract = True
        ordering = ['-created_at', '-updated_at']
