from django.urls import path

from students.views import WhizzerDashboardView, WhizzerQuizDetailView

app_name = "students"
urlpatterns = [
    path('dashboard/', WhizzerDashboardView.as_view(), name='whizzer_dashboard'),
    path('quiz/<uuid:pk>', WhizzerQuizDetailView.as_view(), name='whizzer_quiz_detail'),

]
