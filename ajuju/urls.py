"""
URL configuration for ajuju project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('allauth.urls')),

    path("__reload__/", include("django_browser_reload.urls")),
]
