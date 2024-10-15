"""
This module contains the models for the quiz app.
"""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.models import BaseModel
from teachers.models import Creator


# Create your models here.

class Subject(BaseModel):
    """
    Represents a subject area for quizzes.
    """
    name = models.CharField(
        max_length=255,
        unique=True
    )
    description = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.name


class Quiz(BaseModel):
    """
    Represents a quiz created by a user on a specific subject.
    """
    title = models.CharField(
        max_length=255
    )
    description = models.TextField()
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='quizzes'
    )
    creator = models.ForeignKey(
        Creator,
        on_delete=models.CASCADE,
        related_name='created_quizzes'
    )
    time_limit = models.PositiveIntegerField(
        help_text="Time limit for the quiz in seconds",
        validators=[MinValueValidator(30), MaxValueValidator(3600)]
    )
    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Quizzes"

    def __str__(self):
        return self.title


class Question(BaseModel):
    """
    Represents a single question within a quiz.
    """
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    text = models.TextField()
    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.quiz.title} - Question {self.order}"


class Choice(BaseModel):
    """
    Represents a choice for a multiple-choice question.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    text = models.CharField(
        max_length=200
    )
    is_correct = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.text
