from django.contrib import admin
from .models import Quiz, Pergunta, Score, RespostaUsuario, QuizScore

admin.site.register(Quiz)
admin.site.register(Pergunta)
admin.site.register(Score)
admin.site.register(RespostaUsuario)
admin.site.register(QuizScore)
