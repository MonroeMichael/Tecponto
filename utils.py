from django.db.models import Count, Sum
from .models import Achievement, UserAchievement, PlayerHistory

def check_achievements(user):
    awarded = set(UserAchievement.objects.filter(user=user).values_list('achievement__code', flat=True))

    # 1) Primeiro Passo
    if 'starter' not in awarded:
        if PlayerHistory.objects.filter(user=user).exists():
            grant(user, 'starter')

    # 2) Dez quizzes
    if 'ten_quizzes' not in awarded:
        total = PlayerHistory.objects.filter(user=user).count()
        if total >= 10:
            grant(user, 'ten_quizzes')

    # 3) Cem pontos
    if 'hundred_pts' not in awarded:
        points = PlayerHistory.objects.filter(user=user).aggregate(Sum('score'))['score__sum'] or 0
        if points >= 100:
            grant(user, 'hundred_pts')

def grant(user, code):
    ach = Achievement.objects.get(code=code)
    UserAchievement.objects.create(user=user, achievement=ach)
