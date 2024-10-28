"""
This file contains the views for the teachers app.
"""
from datetime import timedelta

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
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

        # Fetch active whizzers' details
        active_whizzers = QuizAttempt.objects.filter(
            start_time__gte=timezone.now() - timedelta(minutes=30),
            end_time__isnull=True
        ).select_related('whizzer', 'quiz')

        whizzer_details = []
        for attempt in active_whizzers:
            time_left = (attempt.start_time + timedelta(
                minutes=attempt.quiz.time_limit) - timezone.now()).total_seconds()
            whizzer_details.append({
                'username': attempt.whizzer.user.username,
                'quiz_title': attempt.quiz.title,
                'time_left': max(0, int(time_left))
            })

        context['active_whizzers'] = whizzer_details
        context['active_whizzers_count'] = len(whizzer_details)
        return context

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        active_whizzers_count = self.get_context_data()['active_whizzers_count']
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'active_whizzers',
            {
                'type': 'active_whizzers_count',
                'count': active_whizzers_count
            }
        )
        return response


def active_whizzers_api(request):
    active_whizzers = QuizAttempt.objects.filter(
        start_time__gte=timezone.now() - timezone.timedelta(minutes=30),
        end_time__isnull=True
    ).values('whizzer__user')
    return JsonResponse(list(active_whizzers), safe=False)