from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy

from core.views.base_views import CreatorBaseCreateView, CreatorBaseUpdateView, CreatorBaseDeleteView
from quiz.forms.quiz_forms import QuizForm, QuestionFormSet, ChoiceFormSet
from quiz.models import Quiz



class QuizCreateView(CreatorBaseCreateView):
    model = Quiz
    form_class = QuizForm
    template_name ='quiz/quiz_form.html'
    success_url = reverse_lazy('quiz:quiz_index')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['question_formset'] = QuestionFormSet(self.request.POST, instance=self.object)
            data['choice_formset'] = ChoiceFormSet(self.request.POST)
        else:
            data['question_formset'] = QuestionFormSet(instance=self.object)
            data['choice_formset'] = ChoiceFormSet()
        return data

    def form_valid(self, form):

        context = self.get_context_data()
        question_formset = context['question_formset']
        choice_formset = context['choice_formset']
        if form.is_valid() and question_formset.is_valid() and choice_formset.is_valid():
            form.instance.creator = self.request.user.teacher
            self.object = form.save()
            question_formset.instance = self.object
            question_formset.save()
            for question in question_formset:
                choice_formset = ChoiceFormSet(self.request.POST, instance=question.instance)
                if choice_formset.is_valid():
                    choice_formset.save()
                    messages.success(self.request, f"Subject has been created successfully.")
            return redirect(self.success_url)
        else:
            messages.error(self.request, "There was an error creating the subject. Please try again.")
            return self.render_to_response(self.get_context_data(form=form))


class QuizUpdateView(CreatorBaseUpdateView):
    model = Quiz
    form_class = QuizForm
    template_name = 'quiz/quiz_form.html'
    success_url = reverse_lazy('quiz:quiz_index')

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
