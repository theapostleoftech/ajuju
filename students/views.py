"""
This file contains the views for the students app.
"""
from django.utils import timezone

from core.views.base_views import WhizzerBaseTemplateView
from quiz.models import Quiz, QuizAttempt


# Create your views here.
class WhizzerDashboardView(WhizzerBaseTemplateView):
    """
    This is the view for the creator dashboard.
    """
    template_name = 'students/whizzer_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_count'] = Quiz.objects.count()
        context['active_whizzers_count'] = QuizAttempt.objects.filter(
            start_time__gte=timezone.now() - timezone.timedelta(minutes=30),
            end_time__isnull=True
        ).values('whizzer').distinct().count()
        return context

    pass
