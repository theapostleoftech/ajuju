"""
This file contains the views for the students app.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from ajuju.utils.decorators import whizzer_required
from core.views.base_views import WhizzerBaseListView, WhizzerBaseDetailView
from quiz.forms.quiz_forms import QuizAttemptForm
from quiz.models import Quiz, QuizAttempt, Question, Choice, Answer


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


class WhizzerQuizDetailView(WhizzerBaseDetailView):
    """
    This view displays the details of a specific quiz
    """
    model = Quiz
    template_name = 'students/whizzer_quiz_detail.html'
    context_object_name = 'quiz'

    def get_object(self):
        return get_object_or_404(Quiz, pk=self.kwargs['pk'], is_active=True)


@login_required
@whizzer_required
def start_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        form = QuizAttemptForm(request.POST)
        if form.is_valid():
            attempt = form.save(commit=False)
            attempt.quiz = quiz
            attempt.whizzer = request.user.student
            attempt.save()
            return redirect('students:whizzer_take_quiz', attempt_id=attempt.id)
    else:
        form = QuizAttemptForm()
    return render(request, 'students/whizzer_start_quiz.html', {'quiz': quiz, 'form': form})


@login_required
@whizzer_required
def take_quiz(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, whizzer=request.user.student)

    # Redirect if the attempt is completed
    if attempt.is_completed:
        return redirect('students:whizzer_quiz_result', attempt_id=attempt.id)

    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_id = request.POST.get('answer')

        # Validate question and answer submission
        if question_id and answer_id:
            try:
                question = get_object_or_404(Question, id=question_id, quiz=attempt.quiz)
                choice = get_object_or_404(Choice, id=answer_id, question=question)

                # Save the answer
                Answer.objects.update_or_create(
                    attempt=attempt, question=question,
                    defaults={'selected_choice': choice}
                )
            except Http404:
                messages.error(request, "Invalid question or answer.")
                return redirect('students:whizzer_quiz', attempt_id=attempt.id)

            # After saving the answer, retrieve the next question
            question = attempt.quiz.questions.filter(
                ~Q(id__in=attempt.answers.values_list('question__id', flat=True))
            ).first()

            # Check if there are no more questions
            if not question:
                attempt.end_time = timezone.now()
                attempt.score = attempt.calculate_score()
                attempt.save()
                return redirect('students:whizzer_quiz_result', attempt_id=attempt.id)

            # Prepare context for rendering the next question
            context = {
                'attempt': attempt,
                'question': question,
                'time_left': int(attempt.quiz.time_limit - (timezone.now() - attempt.start_time).total_seconds()),
            }
            return render(request, 'students/whizzer_take_quiz.html', context)

        # Handle finishing the quiz
        if 'finish' in request.POST:
            attempt.end_time = timezone.now()
            attempt.score = attempt.calculate_score()
            attempt.save()
            return redirect('students:whizzer_quiz_result', attempt_id=attempt.id)

    # If it's a GET request, retrieve the first question
    question = attempt.quiz.questions.filter(
        ~Q(id__in=attempt.answers.values_list('question__id', flat=True))
    ).first()

    # Check if there are no more questions
    if not question:
        attempt.end_time = timezone.now()
        attempt.score = attempt.calculate_score()
        attempt.save()
        return redirect('students:whizzer_quiz_result', attempt_id=attempt.id)

    # Check time left for the quiz
    time_left = attempt.quiz.time_limit - (timezone.now() - attempt.start_time).total_seconds()
    if time_left <= 0:
        attempt.end_time = timezone.now()
        attempt.score = attempt.calculate_score()
        attempt.save()
        return redirect('students:whizzer_quiz_result', attempt_id=attempt.id)

    # Prepare context for rendering the quiz page
    context = {
        'attempt': attempt,
        'question': question,
        'time_left': int(time_left),
    }
    return render(request, 'students/whizzer_take_quiz.html', context)


# @login_required
# @whizzer_required
# def quiz_result(request, attempt_id):
#     attempt = get_object_or_404(QuizAttempt, id=attempt_id, whizzer=request.user.student)
#     context = {
#         'attempt': attempt,
#         'answers': attempt.answers.all(),
#     }
#     return render(request, 'students/whizzer_quiz_result.html', context)


@login_required
@whizzer_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, whizzer=request.user.student)
    score = attempt.calculate_score()
    total_questions = attempt.total_questions_percentage()

    # Retrieve all answers along with the correct choice for each question
    answers = attempt.answers.all()

    context = {
        'attempt': attempt,
        'answers': answers,
        'score': score,
        'total_questions': total_questions,
    }
    return render(request, 'students/whizzer_quiz_result.html', context)
