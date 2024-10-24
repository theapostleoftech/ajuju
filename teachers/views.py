"""
This file contains the views for the teachers app.
"""
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone

from core.views.base_views import CreatorBaseTemplateView, CreatorBaseListView
from quiz.models import Quiz, Subject, QuizAttempt


# Create your views here.
class CreatorDashboardView(CreatorBaseTemplateView):
    """
    This is the view for the creator dashboard.
    """
    template_name = 'teachers/creator_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_count'] = Quiz.objects.count()
        context['subject_count'] = Subject.objects.count()
        context['active_whizzers_count'] = QuizAttempt.objects.filter(
            start_time__gte=timezone.now() - timezone.timedelta(minutes=30),
            end_time__isnull=True
        ).values('whizzer').distinct().count()
        return context

    pass



class ActiveWhizzerListView(CreatorBaseListView):
    model = QuizAttempt
    template_name = 'teachers/active_whizzers.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_whizzers_count'] = QuizAttempt.objects.filter(
            start_time__gte=timezone.now() - timezone.timedelta(minutes=30),
            end_time__isnull=True
        ).values('whizzer').distinct().count()
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'active_whizzers',
            {
                'type': 'active_whizzers_count',  # This should match the method in the consumer
                'count': self.get_context_data()['active_whizzers_count']
            }
        )
        return response

class SampleView(CreatorBaseTemplateView):
    """
    This is the view for the creator dashboard.
    """
    template_name = 'teachers/sample.html'


class NewView(CreatorBaseTemplateView):
    """
    This is the view for the creator dashboard.
    """
    template_name = 'teachers/new.html'
