from core.views.base_views import CreatorBaseListView
from quiz.models import Quiz


# class QuizIndexView(CreatorBaseTemplateView):
#     template_name = 'quiz/quiz_index.html'
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context['quizzes'] = Quiz.objects.all()
#     #     return context


class SubjectIndexView(CreatorBaseListView):
    model = Quiz
    template_name = 'quiz/subject_index.html'
    context_object_name = 'subjects'


class QuizIndexView(CreatorBaseListView):
    model = Quiz
    template_name = 'quiz/quiz_index.html'
    context_object_name = 'quizzes'
