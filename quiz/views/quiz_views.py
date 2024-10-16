from core.views.base_views import CreatorBaseListView
from quiz.models import Quiz, Subject


# class QuizIndexView(CreatorBaseTemplateView):
#     template_name = 'quiz/quiz_index.html'
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['quizzes'] = Quiz.objects.all()
#     #     return context


class SubjectIndexView(CreatorBaseListView):
    """
    This view is used to display the list of subjects for a creator.
    """
    model = Quiz
    template_name = 'quiz/subject_index.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['subjects'] = Subject.objects.all()
    #     context['subject_count'] = Subject.objects.count()
    #     return context

    context_object_name = 'subjects'

    def get_queryset(self):
        return Subject.objects.filter(creator=self.request.user.teacher)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subject_count'] = self.get_queryset().count()
        return context


class QuizIndexView(CreatorBaseListView):
    """
    This is the view for displaying quizzes.
    """
    model = Quiz
    template_name = 'quiz/quiz_index.html'
    context_object_name = 'quizzes'

    def get_queryset(self):
        return Quiz.objects.filter(creator=self.request.user.teacher)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quiz_count'] = self.get_queryset().count()
        return context
