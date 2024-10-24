from django.urls import path

from teachers.views import CreatorDashboardView, SampleView, NewView, ActiveWhizzerListView

app_name = "teachers"
urlpatterns = [
    path('dashboard/', CreatorDashboardView.as_view(), name='creator_dashboard'),
    path('active_whizzers/', ActiveWhizzerListView.as_view(), name='active_whizzer_list'),
    path('sample/', SampleView.as_view(), name='sample'),
    path('new/', NewView.as_view(), name='new'),
]
