from django.contrib.auth.models import User
from django.db import models

class Quiz(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Score(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    pontuacao = models.IntegerField(default=0)
    tentativas = models.IntegerField(default=0)
    data_jogada = models.DateTimeField(auto_now_add=True)  # Adicionando data do jogo

    def __str__(self):
        return f"{self.usuario.username} - {self.quiz.nome}: {self.pontuacao} pontos"

class Pergunta(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    texto = models.CharField(max_length=255)
    resposta_correta = models.CharField(max_length=100)
    dica = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.texto

class RespostaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    resposta = models.CharField(max_length=100)
    correta = models.BooleanField(default=False)
    pontos_obtidos = models.IntegerField(default=0)
    tempo_resposta = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.usuario.username} - {self.pergunta.texto} - {'Correto' if self.correta else 'Errado'}"
class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
