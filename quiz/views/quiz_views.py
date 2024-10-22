from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from core.views.base_views import CreatorBaseListView
from quiz.models import Quiz, Subject


class SubjectIndexView(CreatorBaseListView):
    """
    This view is used to display the list of subjects for a creator.
    """
    model = Quiz
    template_name = 'quiz/subject_index.html'
    context_object_name = 'subjects'
    paginate_by = 10  # Number of items per page

    def get_queryset(self):
        return Subject.objects.filter(creator=self.request.user.teacher)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            subjects = paginator.page(page)
        except PageNotAnInteger:
            subjects = paginator.page(1)
        except EmptyPage:
            subjects = paginator.page(paginator.num_pages)

        context['subjects'] = subjects
        context['subject_count'] = queryset.count()
        return context


class QuizIndexView(CreatorBaseListView):
    """
    This is the view for displaying quizzes.
    """
    model = Quiz
    template_name = 'quiz/quiz_index.html'
    context_object_name = 'quizzes'
    paginate_by = 10

    def get_queryset(self):
        return Quiz.objects.filter(creator=self.request.user.teacher)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            quizzes = paginator.page(page)
        except PageNotAnInteger:
            quizzes = paginator.page(1)
        except EmptyPage:
            quizzes = paginator.page(paginator.num_pages)
        context['quizzes'] = quizzes
        context['quiz_count'] = queryset.count()
        return context
