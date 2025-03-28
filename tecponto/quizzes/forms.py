from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import RespostaUsuario, Pergunta

# Formulário de Registro de Usuário
class RegistroForm(UserCreationForm):
    username = forms.CharField(label="Nome de usuário", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirme a senha", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# Formulário de Login de Usuário
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nome de usuário", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

# Formulário de Resposta de Quiz
class RespostaQuizForm(forms.ModelForm):
    class Meta:
        model = RespostaUsuario
        fields = ['pergunta', 'resposta']
        widgets = {
            'pergunta': forms.HiddenInput(),  # A pergunta já virá preenchida
            'resposta': forms.RadioSelect(),  # Exibir opções como botões de rádio
        }
