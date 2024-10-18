"""
This file contains the views for the students app.
"""
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['quiz_count'] = Quiz.objects.count()
    #     context['active_whizzers_count'] = QuizAttempt.objects.filter(
    #         start_time__gte=timezone.now() - timezone.timedelta(minutes=30),
    #         end_time__isnull=True
    #     ).values('whizzer').distinct().count()
    #     return context


class WhizzerQuizDetailView(WhizzerBaseDetailView):
    """
    This view displays the details of a specific quiz
    """
    model = Quiz
    template_name = 'students/whizzer_quiz_detail.html'
    context_object_name = 'quiz'

    def get_object(self):
        return get_object_or_404(Quiz, pk=self.kwargs['pk'], is_active=True)


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


def take_quiz(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, whizzer=request.user.student)
    if attempt.is_completed:
        return redirect('students:whizzer_quiz_result', attempt_id=attempt.id)

    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        answer_id = request.POST.get('answer')
        if question_id and answer_id:
            question = get_object_or_404(Question, id=question_id, quiz=attempt.quiz)
            choice = get_object_or_404(Choice, id=answer_id, question=question)
            Answer.objects.update_or_create(
                attempt=attempt, question=question,
                defaults={'selected_choice': choice}
            )

        if 'finish' in request.POST:
            attempt.end_time = timezone.now()
            attempt.score = attempt.calculate_score()
            attempt.save()
            return redirect('students:whizzer_quiz_result', attempt_id=attempt.id)

    question = attempt.quiz.questions.filter(
        ~Q(id__in=attempt.answers.values_list('question__id', flat=True))
    ).first()

    if not question:
        attempt.end_time = timezone.now()
        attempt.score = attempt.calculate_score()
        attempt.save()
        return redirect('students:whizzer_quiz_result', attempt_id=attempt.id)

    time_left = attempt.quiz.time_limit - (timezone.now() - attempt.start_time).total_seconds()
    if time_left <= 0:
        attempt.end_time = timezone.now()
        attempt.score = attempt.calculate_score()
        attempt.save()
        return redirect('students:whizzer_quiz_result', attempt_id=attempt.id)

    context = {
        'attempt': attempt,
        'question': question,
        'time_left': int(time_left),
    }
    return render(request, 'students/whizzer_take_quiz.html', context)


def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, whizzer=request.user.student)
    context = {
        'attempt': attempt,
        'answers': attempt.answers.all(),
    }
    return render(request, 'students/whizzer_quiz_result.html', context)
