from django.urls import path

from teachers.views import CreatorDashboardView, SampleView, NewView

app_name = "teachers"
urlpatterns = [
    path('dashboard/', CreatorDashboardView.as_view(), name='creator_dashboard'),
    path('sample/', SampleView.as_view(), name='sample'),
    path('new/', NewView.as_view(), name='new'),
]
