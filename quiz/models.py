"""
This module contains the models for the quiz app.
"""
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from core.models import BaseModel
from students.models import Whizzer
from teachers.models import Creator


# Create your models here.

class Subject(BaseModel):
    """
    Represents a subject area for quizzes.
    """
    creator = models.ForeignKey(
        Creator,
        on_delete=models.CASCADE,
        null=True,
        related_name='created_subjects'
    )
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
        related_name='teacher'
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
        max_length=255
    )
    is_correct = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.text


class QuizAttempt(BaseModel):
    """
    Represents an attempt by a user (whizzer) to take a quiz.
    """
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    whizzer = models.ForeignKey(
        Whizzer,
        on_delete=models.CASCADE,
        related_name='quiz_attempts'
    )
    start_time = models.DateTimeField(
        default=timezone.now
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True
    )
    score = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.whizzer.user.username}'s attempt on {self.quiz.title}"

    @property
    def is_completed(self):
        return self.end_time is not None

    @property
    def time_taken(self):
        if self.is_completed:
            return (self.end_time - self.start_time).total_seconds()
        return None


class Answer(BaseModel):
    """
    Represents a user's answer to a question during a quiz attempt.
    """
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    selected_choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE
    )
    answered_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ['attempt', 'question']

    def __str__(self):
        return f"Answer to {self.question} by {self.attempt.whizzer.user.username}"
