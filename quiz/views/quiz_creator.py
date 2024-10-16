from django.db import transaction
from django.urls import reverse_lazy

from core.views.base_views import CreatorBaseCreateView, CreatorBaseUpdateView, CreatorBaseDeleteView
from quiz.forms import QuizForm, QuestionFormSet
from quiz.models import Quiz


class QuizCreateView(CreatorBaseCreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quiz/quiz_form.html'
    success_url = reverse_lazy('quiz_list')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class QuizUpdateView(CreatorBaseUpdateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quiz/quiz_form.html'
    success_url = reverse_lazy('quiz_list')

    def test_func(self):
        quiz = self.get_object()
        return self.request.user == quiz.creator

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['questions'] = QuestionFormSet(self.request.POST, instance=self.object)
        else:
            data['questions'] = QuestionFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        questions = context['questions']
        with transaction.atomic():
            self.object = form.save()
            if questions.is_valid():
                questions.instance = self.object
                questions.save()
        return super().form_valid(form)


class QuizDeleteView(CreatorBaseDeleteView):
    model = Quiz
    success_url = reverse_lazy('quiz_list')
    template_name = 'quiz/quiz_confirm_delete.html'

    def test_func(self):
        quiz = self.get_object()
        return self.request.user == quiz.creator
