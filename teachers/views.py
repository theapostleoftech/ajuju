"""
This file contains the views for the teachers app.
"""
from django.shortcuts import render

from core.views.base_views import CreatorBaseTemplateView


# Create your views here.
class CreatorDashboardView(CreatorBaseTemplateView):
    """
    This is the view for the creator dashboard.
    """
    template_name = 'teachers/creator_dashboard.html'
    pass
