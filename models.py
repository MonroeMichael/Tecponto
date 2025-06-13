from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# ---------- USUÁRIO PERSONALIZADO ----------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# ---------- CONTEÚDO ----------
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    title      = models.CharField(max_length=200)
    subject    = models.ForeignKey(Subject, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=20, choices=[
        ('Fácil', 'Fácil'), ('Médio', 'Médio'), ('Difícil', 'Difícil')
    ])
    help_link  = models.URLField(blank=True, null=True)     # link opcional

    def __str__(self):
        return f"{self.title} ({self.subject})"


class Question(models.Model):
    quiz  = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text  = models.TextField()
    hint  = models.TextField(blank=True)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question   = models.ForeignKey(Question, on_delete=models.CASCADE)
    text       = models.CharField(max_length=300)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


# ---------- HISTÓRICO ----------
class PlayerHistory(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quiz        = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score       = models.IntegerField(default=0)
    attempts    = models.IntegerField(default=0)
    last_played = models.DateTimeField(auto_now=True)
    finalizado  = models.BooleanField(default=False)      # ✓ novo campo

    def __str__(self):
        return f"{self.user.email} - {self.quiz.title} - {self.score} pts"


def total_points(user):
    return (PlayerHistory.objects
            .filter(user=user, finalizado=True)
            .aggregate(Sum('score'))['score__sum'] or 0)


# ---------- CONQUISTAS ----------
class Achievement(models.Model):
    RULE_CHOICES = [
        ('quizzes', 'Total de partidas'),
        ('points',  'Pontos acumulados'),
    ]

    code       = models.CharField(max_length=50, unique=True)
    name       = models.CharField(max_length=100)
    icon       = models.CharField(max_length=100, default="🏅")
    rule       = models.CharField(max_length=50, choices=RULE_CHOICES)
    threshold  = models.PositiveIntegerField(default=1)

    users = models.ManyToManyField(CustomUser, through='UserAchievement')

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    user        = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_awarded = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')
