from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy

from core.views.base_views import CreatorBaseCreateView, CreatorBaseUpdateView, CreatorBaseDeleteView
from quiz.forms.quiz_forms import QuizForm, QuestionFormSet
from quiz.models import Quiz


class QuizCreateView(CreatorBaseCreateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quiz/quiz_form.html'
    success_url = reverse_lazy('quiz:quiz_index')

    def form_valid(self, form):
        form.instance.creator = self.request.user.teacher
        messages.success(self.request, f"Subject has been created successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the subject. Please try again.")
        return super().form_invalid(form)


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
