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

    def get_time_limit_display(self):
        # Convert time limit to minutes or hours
        if self.time_limit >= 3600:  # 1 hour or more
            hours = self.time_limit // 3600
            if hours == 1:
                return f"{hours} hour"
            else:
                return f"{hours} hours"
        elif self.time_limit >= 60:  # More than 1 minute
            minutes = self.time_limit // 60
            if minutes == 1:
                return f"{minutes} minute"
            else:
                return f"{minutes} minutes"
        else:
            return f"{self.time_limit} second(s)"


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

    # order = models.PositiveIntegerField(
    #     default=0
    # )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:50]}"


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

    def calculate_score(self):
        # Get the total number of questions in the quiz
        total_questions = self.quiz.questions.count()

        # Get the number of correct answers
        correct_answers = self.answers.filter(selected_choice__is_correct=True).count()

        # Calculate the score as a percentage
        if total_questions > 0:
            score_percentage = (correct_answers / total_questions) * 100  # Convert to percentage
        else:
            score_percentage = 0  # No questions, score is 0

        # Round to 2 decimal places
        return round(score_percentage, 2)

    def total_questions_percentage(self):
        """Return the total questions as a percentage."""
        total_questions = self.quiz.questions.count()
        return 100.0 if total_questions > 0 else 0.0

    def get_result_summary(self):
        total_questions = self.quiz.questions.count()
        answered_questions = self.answers.count()
        correct_answers = self.answers.filter(selected_choice__is_correct=True).count()

        # Ensure no negative values
        incorrect_answers = max(0, answered_questions - correct_answers)
        unanswered_questions = max(0, total_questions - answered_questions)

        return {
            'total_questions': total_questions,
            'answered_questions': answered_questions,
            'correct_answers': correct_answers,
            'incorrect_answers': incorrect_answers,
            'unanswered_questions': unanswered_questions,
            'score': self.calculate_score(),
        }


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
