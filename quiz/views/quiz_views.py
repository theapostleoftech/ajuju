from django.views.generic import TemplateView


class QuizIndexView(TemplateView):
    template_name = 'quiz/quiz_index.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['quizzes'] = Quiz.objects.all()
    #     return context
