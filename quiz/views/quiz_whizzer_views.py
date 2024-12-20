from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from quiz.forms.quiz_forms import QuizAttemptForm
from quiz.models import Quiz, QuizAttempt, Question, Choice, Answer


def start_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    if request.method == 'POST':
        form = QuizAttemptForm(request.POST)
        if form.is_valid():
            attempt = form.save(commit=False)
            attempt.quiz = quiz
            attempt.whizzer = request.user.student
            attempt.save()
            return redirect('take_quiz', attempt_id=attempt.id)
    else:
        form = QuizAttemptForm()
    return render(request, 'quiz/start_quiz.html', {'quiz': quiz, 'form': form})


def take_quiz(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, whizzer=request.user)
    if attempt.is_completed:
        return redirect('quiz_result', attempt_id=attempt.id)

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
            return redirect('quiz_result', attempt_id=attempt.id)

    question = attempt.quiz.questions.filter(
        ~Q(id__in=attempt.answers.values_list('question__id', flat=True))
    ).first()

    if not question:
        attempt.end_time = timezone.now()
        attempt.score = attempt.calculate_score()
        attempt.save()
        return redirect('quiz_result', attempt_id=attempt.id)

    time_left = attempt.quiz.time_limit - (timezone.now() - attempt.start_time).total_seconds()
    if time_left <= 0:
        attempt.end_time = timezone.now()
        attempt.score = attempt.calculate_score()
        attempt.save()
        return redirect('quiz_result', attempt_id=attempt.id)

    context = {
        'attempt': attempt,
        'question': question,
        'time_left': int(time_left),
    }
    return render(request, 'quiz/take_quiz.html', context)


def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, whizzer=request.user)
    context = {
        'attempt': attempt,
        'answers': attempt.answers.all(),
    }
    return render(request, 'quiz/quiz_result.html', context)
