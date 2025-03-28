from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    home, login_view, registro, pagina_usuario, quiz, 
    meus_quizzes, save_score, user_scores
)
from .views import lista_quizzes

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("", home, name="home"),  # Página inicial
    path("registro/", registro, name="registro"),
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),  # Redireciona para home ao deslogar
    path("usuario/", pagina_usuario, name="pagina_usuario"),
    path("quiz/<int:quiz_id>/", quiz, name="quiz"),
    path("meus_quizzes/", meus_quizzes, name="meus_quizzes"),
    path("save_score/", save_score, name="save_score"),
    path("user_scores/", user_scores, name="user_scores"),
]