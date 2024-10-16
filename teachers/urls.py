from django.urls import path

from teachers.views import CreatorDashboardView

app_name = "teachers"
urlpatterns = [
    path('dashboard/', CreatorDashboardView.as_view(), name='creator_dashboard'),
]
