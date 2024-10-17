"""
This file contains the views for the students app.
"""
from django.shortcuts import get_object_or_404

from core.views.base_views import WhizzerBaseListView, WhizzerBaseDetailView
from quiz.models import Quiz


# Create your views here.
class WhizzerDashboardView(WhizzerBaseListView):
    """
    This view lists all the available quizzes that can be taken by a whizzer.
    """
    model = Quiz
    template_name = 'students/whizzer_dashboard.html'
    context_object_name = 'quizzes'

    def get_queryset(self):
        return Quiz.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['quiz_count'] = Quiz.objects.count()
    #     context['active_whizzers_count'] = QuizAttempt.objects.filter(
    #         start_time__gte=timezone.now() - timezone.timedelta(minutes=30),
    #         end_time__isnull=True
    #     ).values('whizzer').distinct().count()
    #     return context


class WhizzerQuizDetailView(WhizzerBaseDetailView):
    """
    This view displays the details of a specific quiz
    """
    model = Quiz
    template_name = 'students/whizzer_quiz_detail.html'
    context_object_name = 'quiz'

    def get_object(self):
        return get_object_or_404(Quiz, pk=self.kwargs['pk'], is_active=True)
