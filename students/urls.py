from django.urls import path

from students.views import WhizzerDashboardView

app_name = "students"
urlpatterns = [
    path('dashboard/', WhizzerDashboardView.as_view(), name='whizzer_dashboard'),
]
