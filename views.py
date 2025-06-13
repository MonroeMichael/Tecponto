from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q, Sum
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import (
    Quiz, Question, Answer, PlayerHistory, Subject,
    UserAchievement
)
from .utils import check_achievements


# ---------- JOGAR QUIZ ----------
@login_required
def play_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    total = questions.count()

    current = int(request.GET.get("q", 1))
    hist_key = f"history_{quiz.id}"
    attempts_key = f"quiz_{quiz.id}_attempts"
    attempts_dict = request.session.get(attempts_key, {})

    # Verifica se o jogador já finalizou esse quiz anteriormente
    if current == 1:
        # Se o histórico ainda está em progresso, reutiliza
        if hist_key in request.session:
            hist_id = request.session[hist_key]
            history = get_object_or_404(PlayerHistory, id=hist_id)
        # Caso contrário, impede repetir se já finalizou
        elif PlayerHistory.objects.filter(user=request.user, quiz=quiz).exists():
            return redirect('finish_quiz', quiz_id=quiz.id)
        else:
            request.session.pop(attempts_key, None)
            history = PlayerHistory.objects.create(
                user=request.user, quiz=quiz, score=0, attempts=0
            )
            request.session[hist_key] = history.id
    else:
        hist_id = request.session.get(hist_key)
        history = get_object_or_404(PlayerHistory, id=hist_id)

    if current > total:
        return redirect('finish_quiz', quiz_id=quiz.id)

    question = questions[current - 1]
    answers = Answer.objects.filter(question=question)

    if request.method == "POST":
        selected_id = int(request.POST.get("answer"))
        selected_answer = Answer.objects.get(id=selected_id)

        attempts_dict[str(question.id)] = attempts_dict.get(str(question.id), 0) + 1
        request.session[attempts_key] = attempts_dict

        if selected_answer.is_correct:
            tries = attempts_dict[str(question.id)]
            earned = 10 if tries == 1 else 5 if tries == 2 else 2

            history.score += earned
            history.attempts += tries
            history.last_played = timezone.now()
            history.save()

            attempts_dict.pop(str(question.id))
            request.session[attempts_key] = attempts_dict
            return redirect(f"/quiz/{quiz.id}/?q={current + 1}")

        return render(request, "quiz/play.html", {
            "quiz": quiz, "question": question, "answers": answers,
            "error": "Resposta incorreta!", "hint": question.hint
        })

    return render(request, "quiz/play.html", {
        "quiz": quiz, "question": question, "answers": answers
    })



# ---------- LISTA DE QUIZZES ----------
def quiz_list(request):
    quizzes = Quiz.objects.all()
    search = request.GET.get('q', '')
    subj_id = request.GET.get('subject')
    diff = request.GET.get('difficulty')

    if search:
        quizzes = quizzes.filter(
            Q(title__icontains=search) | Q(question__text__icontains=search)
        ).distinct()
    if subj_id:
        quizzes = quizzes.filter(subject_id=subj_id)
    if diff:
        quizzes = quizzes.filter(difficulty=diff)

    return render(request, 'quiz/quiz_list.html', {
        'quizzes': quizzes,
        'subjects': Subject.objects.all(),
        'difficulties': [('Fácil','Fácil'), ('Médio','Médio'), ('Difícil','Difícil')],
    })


# ---------- TELA FINAL ----------
@login_required
def finish_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    hist_id = request.session.pop(f"history_{quiz.id}", None)
    history = get_object_or_404(PlayerHistory, id=hist_id) if hist_id else None

    if history and not history.finalizado:
        history.finalizado = True
        history.save()
        check_achievements(request.user)

    return render(request, 'quiz/finish.html', {'quiz': quiz, 'history': history})



# ---------- CADASTRO ----------
from .forms import CustomUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quiz_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# ---------- PERFIL ----------
@login_required
def profile(request):
    user = request.user
    histories = PlayerHistory.objects.filter(
        user=user,
        finalizado=True  # ⬅️ Só exibe quizzes finalizados
    ).select_related('quiz', 'quiz__subject').order_by('-last_played')

    total_points = histories.aggregate(Sum('score'))['score__sum'] or 0
    quizzes_done = histories.values('quiz').distinct().count()
    achievements = UserAchievement.objects.filter(user=user).select_related('achievement')

    context = {
        'total_points': total_points,
        'quizzes_done': quizzes_done,
        'histories': histories[:10],
        'achievements': achievements,
    }
    return render(request, 'quiz/profile.html', context)

# ---------- comfigurações ----------
def conf_view(request):
    return render(request, 'registration/conf.html')


signup

# ---------- Ranking ----------

@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect('quiz_list')

@login_required
def player(request):
    return render(request, 'quiz/player.html')

@login_required
def ranking(request):
    rankings = (
        PlayerHistory.objects
        .filter(finalizado=True)  # ⬅️ Apenas quizzes concluídos
        .values('user__email')
        .annotate(total_points=Sum('score'))
        .order_by('-total_points')[:10]
    )
    return render(request, 'quiz/ranking.html', {'rankings': rankings})

# ---------- Video Apoio ----------


@login_required
def finish_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    hist_id = request.session.pop(f"history_{quiz.id}", None)
    history = get_object_or_404(PlayerHistory, id=hist_id) if hist_id else None

    help_message = None
    help_link = None

    if history and not history.finalizado:
        history.finalizado = True
        history.save()
        check_achievements(request.user)
        total_questions = quiz.question_set.count()
        max_score = total_questions * 10
        score_percent = (history.score / max_score) * 100 if max_score else 0

        if score_percent < 60 and quiz.help_link:
            help_link = quiz.help_link
            help_message = "Poxa que pena... Não desanime! Aqui vai um link pra você mandar bem da próxima vez:"

    return render(request, 'quiz/finish.html', {
        'quiz': quiz,
        'history': history,
        'help_message': help_message,
        'help_link': help_link,
    })
