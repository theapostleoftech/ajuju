from django.urls import path

from quiz.views import quiz_views, quiz_creator

app_name = 'quiz'
urlpatterns = [
    path('', quiz_views.QuizIndexView.as_view(), name='quiz_index'),
    # path('quiz/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz/new/', quiz_creator.QuizCreateView.as_view(), name='quiz_create'),
    path('quiz/update/<uuid:pk>/', quiz_creator.QuizUpdateView.as_view(), name='quiz_update'),
    path('quiz/delete/<uuid:pk>/', quiz_creator.QuizDeleteView.as_view(), name='quiz_delete'),
    # path('quiz/<int:pk>/start/', views.start_quiz, name='start_quiz'),
    # path('quiz/attempt/<int:attempt_id>/', views.take_quiz, name='take_quiz'),
    # path('quiz/result/<int:attempt_id>/', views.quiz_result, name='quiz_result'),
]
