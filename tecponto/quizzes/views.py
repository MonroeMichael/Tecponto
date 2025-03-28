from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Quiz, Pergunta, RespostaUsuario, Score
from .forms import RegistroForm

@login_required
def meus_quizzes(request):
    quizzes = Quiz.objects.all()  # Mostra todos os quizzes disponíveis
    return render(request, "quizzes/meus_quizzes.html", {"quizzes": quizzes})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("pagina_usuario")  
    else:
        form = AuthenticationForm()
    return render(request, "quizzes/login.html", {"form": form})

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("pagina_usuario")
    else:
        form = RegistroForm()
    return render(request, "quizzes/registro.html", {"form": form})

@login_required
def pagina_usuario(request):
    return render(request, "quizzes/pagina_usuario.html")

def home(request):
    return render(request, "quizzes/home.html")

@login_required
def quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    perguntas = Pergunta.objects.filter(quiz=quiz).order_by("?")
    return render(request, "quizzes/quiz.html", {"quiz": quiz, "perguntas": perguntas})

@csrf_exempt
@login_required
def save_score(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            quiz_id = data.get("quiz_id")
            score = data.get("score")

            if quiz_id is None or score is None:
                return JsonResponse({"error": "Dados inválidos"}, status=400)

            quiz = get_object_or_404(Quiz, id=quiz_id)

            # Salva ou atualiza a pontuação do usuário para esse quiz
            score_obj, created = Score.objects.get_or_create(usuario=request.user, quiz=quiz)
            score_obj.pontuacao = max(score_obj.pontuacao, score)  # Mantém a maior pontuação
            score_obj.tentativas += 1
            score_obj.save()

            return JsonResponse({"message": "Pontuação salva com sucesso!"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)

    return JsonResponse({"error": "Método não permitido"}, status=405)

@login_required
def user_scores(request):
    scores = Score.objects.filter(usuario=request.user).order_by("-played_at")
    scores_list = [
        {
            "quiz_name": s.quiz.nome,
            "score": s.pontuacao,
            "tentativas": s.tentativas,
            "played_at": s.played_at.strftime("%Y-%m-%d %H:%M"),
        }
        for s in scores
    ]

    return JsonResponse({"scores": scores_list})

def lista_quizzes(request):
    quizzes = Quiz.objects.all()  # Busca todos os quizzes do banco
    return render(request, 'quizzes/lista_quizzes.html', {'quizzes': quizzes})


@login_required
def finalizacao(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    score = Score.objects.filter(usuario=request.user, quiz=quiz).first()

    return render(request, "quizzes/finalizacao.html", {"quiz": quiz, "score": score})