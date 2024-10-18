from django.contrib import admin

from quiz.models import Subject, Quiz, Question, Choice, Answer, QuizAttempt

# Register your models here.

admin.site.register(Subject)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)
admin.site.register(QuizAttempt)
