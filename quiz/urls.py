from django.urls import path

from quiz.views import quiz_views

urlpatterns = [
    path('quiz/', quiz_views.QuizIndexView.as_view(), name='quiz_index'),
]