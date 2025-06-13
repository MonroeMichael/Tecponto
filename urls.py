from . import views
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('perfil/', views.profile, name='profile'),          
    path('signup/', views.signup, name='signup'),
    path('<int:quiz_id>/', views.play_quiz, name='play_quiz'),
    path('<int:quiz_id>/finish/', views.finish_quiz, name='finish_quiz'),
    path('logout/', views.logout_view, name='logout'),
    path('conf/', views.conf_view, name='conf'),
    path('player/', views.player, name='player'),
    path('ranking/', views.ranking, name='ranking'),
]
