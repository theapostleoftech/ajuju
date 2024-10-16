from django.urls import path

from core.views import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
