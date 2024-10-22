import logging

from django import forms
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from formtools.wizard.views import SessionWizardView

from core.views.base_views import CreatorBaseUpdateView, CreatorBaseDeleteView
from quiz.forms.quiz_forms import QuizForm, QuestionFormSet, QuestionForm, ChoiceForm
from quiz.models import Quiz

logger = logging.getLogger(__name__)


# class QuizCreateWizard(SessionWizardView):
#     """
#     This view handles the creation of a quiz, allowing the user to dynamically
#     add multiple questions and their corresponding choices before submission.
#     """
#
#     form_list = [
#         ('quiz', QuizForm),
#         ('questions_and_choices', forms.Form),
#     ]
#     template_name = 'quiz/quiz_create_wizard.html'
#
#     def get_form_initial(self, step):
#         initial = super().get_form_initial(step)
#         if step == 'quiz':
#             initial['creator'] = self.request.user.id
#         return initial
#
#     def get_context_data(self, form, **kwargs):
#         context = super().get_context_data(form=form, **kwargs)
#         if self.steps.current == 'questions_and_choices':
#             context['question_form'] = QuestionForm(prefix='question')
#             context['choice_forms'] = [ChoiceForm(prefix=f'choice_{i}') for i in range(4)]
#         return context
#
#     def process_step(self, form):
#         if self.steps.current == 'questions_and_choices':
#             # Process the questions and choices data
#             questions_data = self.request.POST.getlist('question_text')
#             choices_data = self.request.POST.getlist('choice_text')
#             is_correct_data = self.request.POST.getlist('is_correct')
#
#             logger.debug(f"Processed questions: {questions_data}")
#             logger.debug(f"Processed choices: {choices_data}")
#             logger.debug(f"Processed is_correct: {is_correct_data}")
#
#             # Store the processed data in the wizard's storage
#             self.storage.set_step_data('questions_and_choices', {
#                 'questions': questions_data,
#                 'choices': choices_data,
#                 'is_correct': is_correct_data
#             })
#
#         return self.get_form_step_data(form)
#
#     def done(self, form_list, **kwargs):
#         try:
#             quiz_form = form_list[0]
#             questions_and_choices_data = self.storage.get_step_data('questions_and_choices')
#
#             # Save the quiz
#             quiz = quiz_form.save(commit=False)
#             quiz.creator = self.request.user.teacher
#             quiz.save()
#             logger.info(f"Created new quiz: {quiz.title} by user {self.request.user.username}")
#
#             # Process questions and choices
#             questions_data = questions_and_choices_data.getlist('questions')
#             choices_data = questions_and_choices_data.getlist('choices')
#             is_correct_data = questions_and_choices_data.getlist('is_correct')
#
#             logger.debug(f"Questions data: {questions_data}")
#             logger.debug(f"Choices data: {choices_data}")
#             logger.debug(f"Is correct data: {is_correct_data}")
#
#             for i, question_text in enumerate(questions_data):
#                 if question_text:  # Only create question if text is provided
#                     question = Question(quiz=quiz, text=question_text)
#                     question.save()
#                     logger.info(f"Added question to quiz {quiz.id}: {question.text}")
#
#                     # Process choices for this question
#                     choice_start = i * 4
#                     choice_end = min(choice_start + 4, len(choices_data))
#                     question_choices = choices_data[choice_start:choice_end]
#                     question_is_correct = is_correct_data[choice_start:choice_end]
#
#                     for j, (choice_text, is_correct) in enumerate(zip(question_choices, question_is_correct)):
#                         if choice_text:  # Only create choice if text is provided
#                             choice = Choice(
#                                 question=question,
#                                 text=choice_text,
#                                 is_correct=(is_correct == 'on')
#                             )
#                             choice.save()
#                             logger.info(
#                                 f"Added choice to question {question.id}: {choice.text}, is_correct: {choice.is_correct}")
#
#             messages.success(self.request, "Quiz created successfully!")
#             return redirect(reverse_lazy('quiz:quiz_index'))
#
#         except Exception as e:
#             logger.error(f"Error creating quiz: {str(e)}", exc_info=True)
#             messages.error(self.request, "An error occurred while creating the quiz. Please try again.")
#             return self.render_to_response(self.get_context_data(form=form_list[0]))


class QuizCreateWizard(SessionWizardView):
    form_list = [
        ('quiz', QuizForm),
        ('questions_and_choices', forms.Form),
    ]
    template_name = 'quiz/quiz_create_wizard.html'

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)
        if step == 'quiz':
            initial['creator'] = self.request.user.id
        return initial

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == 'questions_and_choices':
            context['question_forms'] = [QuestionForm(prefix=f'question_{i}') for i in
                                         range(5)]  # Allow up to 5 questions
            context['choice_forms'] = [[ChoiceForm(prefix=f'question_{i}_choice_{j}') for j in range(4)] for i in
                                       range(5)]
        return context

    def process_step(self, form):
        return self.get_form_step_data(form)

    def done(self, form_list, **kwargs):
        try:
            quiz_form = form_list[0]

            # Save the quiz
            quiz = quiz_form.save(commit=False)
            quiz.creator = self.request.user.teacher
            quiz.save()
            logger.info(f"Created new quiz: {quiz.title} by user {self.request.user.username}")

            # Process questions and choices
            for i in range(5):  # Up to 5 questions
                question_form = QuestionForm(self.request.POST, prefix=f'question_{i}')
                if question_form.is_valid() and question_form.cleaned_data.get('text'):
                    question = question_form.save(commit=False)
                    question.quiz = quiz
                    question.save()
                    logger.info(f"Added question to quiz {quiz.id}: {question.text}")

                    # Process choices for this question
                    for j in range(4):  # 4 choices per question
                        choice_form = ChoiceForm(self.request.POST, prefix=f'question_{i}_choice_{j}')
                        if choice_form.is_valid() and choice_form.cleaned_data.get('text'):
                            choice = choice_form.save(commit=False)
                            choice.question = question
                            choice.save()
                            logger.info(
                                f"Added choice to question {question.id}: {choice.text}, is_correct: {choice.is_correct}")

            messages.success(self.request, "Quiz created successfully!")
            return redirect(reverse_lazy('quiz:quiz_index'))

        except Exception as e:
            logger.error(f"Error creating quiz: {str(e)}", exc_info=True)
            messages.error(self.request, "An error occurred while creating the quiz. Please try again.")
            return self.render_to_response(self.get_context_data(form=form_list[0]))


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
