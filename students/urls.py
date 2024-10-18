from django.urls import path

from students.views import WhizzerDashboardView, WhizzerQuizDetailView, start_quiz, quiz_result, take_quiz

app_name = "students"
urlpatterns = [
    path('dashboard/', WhizzerDashboardView.as_view(), name='whizzer_dashboard'),
    path('quiz/<uuid:pk>', WhizzerQuizDetailView.as_view(), name='whizzer_quiz_detail'),

    path('quiz/start/<uuid:pk>', start_quiz, name='whizzer_start_quiz'),

    path('quiz/attempt/<uuid:attempt_id>/', take_quiz, name='whizzer_take_quiz'),
    path('quiz/result/<uuid:attempt_id>/', quiz_result, name='whizzer_quiz_result'),

]
