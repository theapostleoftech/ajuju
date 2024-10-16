"""
URL configuration for ajuju project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

    path('creators/', include('teachers.urls', namespace='teachers')),
    path('whizzers/', include('students.urls', namespace='students')),
    path('users/', include('users.urls', namespace='users')),

    path('quizzes/', include('quiz.urls', namespace='quiz')),

    path("__reload__/", include("django_browser_reload.urls")),
]
