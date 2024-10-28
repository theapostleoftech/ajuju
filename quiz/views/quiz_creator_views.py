import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy

from core.views.base_views import CreatorBaseDeleteView
from quiz.forms.quiz_forms import QuizForm, ChoiceFormSet, QuestionFormSet
from quiz.models import Quiz, Question, Choice

logger = logging.getLogger(__name__)


@login_required
def create_quiz_view(request):
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST, prefix='questions')


        if quiz_form.is_valid() and question_formset.is_valid():
            quiz = quiz_form.save(commit=False)
            quiz.creator = request.user.teacher
            quiz.save()

            questions = question_formset.save(commit=False)

            for i, question in enumerate(questions):
                question.quiz = quiz
                question.save()

                # Handle choices for each question
                choice_formset = ChoiceFormSet(
                    request.POST,
                    prefix=f'choices-{i}'
                )
                if choice_formset.is_valid():
                    choices = choice_formset.save(commit=False)
                    for choice in choices:
                        choice.question = question
                        choice.save()
                else:
                    # Handle invalid choice formset
                    return render(request, 'quiz/quiz_create_wizard.html', {
                        'quiz_form': quiz_form,
                        'question_formset': question_formset,
                        'choice_formset': choice_formset,
                        'errors': choice_formset.errors,
                    })

            return redirect('quiz:quiz_index')
    else:
        # Create fresh instances for a new quiz
        quiz_form = QuizForm()
        question_formset = QuestionFormSet(prefix='questions', queryset=Question.objects.none())
        choice_formset = ChoiceFormSet(prefix='choices-0', queryset=Choice.objects.none())

    return render(request, 'quiz/quiz_create_wizard.html', {
        'quiz_form': quiz_form,
        'question_formset': question_formset,
        'choice_formset': choice_formset,
    })


@login_required
def edit_quiz_view(request, quiz_id):
    # Retrieve the existing quiz instance
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        # Load existing data into forms
        quiz_form = QuizForm(request.POST, instance=quiz)
        question_formset = QuestionFormSet(request.POST, prefix='questions', queryset=quiz.questions.all())

        if quiz_form.is_valid() and question_formset.is_valid():
            # Save the updated quiz
            quiz = quiz_form.save()

            # Save the questions
            questions = question_formset.save(commit=False)
            for question in questions:
                question.quiz = quiz
                question.save()

                # Handle choices for each question
                choice_formset = ChoiceFormSet(
                    request.POST,
                    prefix=f'choices-{question.id}',  # Use question ID for prefix
                    queryset=question.choices.all()
                )
                if choice_formset.is_valid():
                    choices = choice_formset.save(commit=False)
                    for choice in choices:
                        choice.question = question
                        choice.save()
                else:
                    # Handle invalid choice formset
                    return render(request, 'quiz/quiz_edit.html', {
                        'quiz_form': quiz_form,
                        'question_formset': question_formset,
                        'choice_formset': choice_formset,
                        'errors': choice_formset.errors,
                    })

            return redirect('quiz:quiz_index')
        else:
            # Handle invalid quiz form or question formset
            return render(request, 'quiz/quiz_edit.html', {
                'quiz_form': quiz_form,
                'question_formset': question_formset,
                'errors': quiz_form.errors,
            })
    else:
        # Initialize forms with existing quiz data
        quiz_form = QuizForm(instance=quiz)
        question_formset = QuestionFormSet(prefix='questions', queryset=quiz.questions.all())
        # Initialize choice formsets for each question
        choice_formsets = [ChoiceFormSet(prefix=f'choices-{question.id}', queryset=question.choices.all()) for question
                           in quiz.questions.all()]

    return render(request, 'quiz/quiz_edit.html', {
        'quiz_form': quiz_form,
        'question_formset': question_formset,
        'choice_formsets': choice_formsets,
    })


class QuizDeleteView(CreatorBaseDeleteView):
    """
    This view is used to delete quizes
    """
    model = Quiz
    success_url = reverse_lazy('quiz:quiz_index')
    template_name = 'quiz/quiz_confirm_delete.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "The quiz was deleted successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "There was an error deleting the quiz.")
        return super().form_invalid(form)
