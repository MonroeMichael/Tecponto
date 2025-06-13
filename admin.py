from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from .models import (
    CustomUser, Subject, Quiz, Question,
    Answer, PlayerHistory, Achievement, UserAchievement
)

# ------------ Custom User ------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Permissões'), {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Datas importantes'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

# ------------ Subject ------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# ------------ Quiz ------------
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject')
    search_fields = ('title',)

# ------------ Question ------------
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz')
    search_fields = ('text',)

# ------------ Answer ------------
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    search_fields = ('text',)

# ------------ User Achievement ------------
@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'date_awarded')
    search_fields = ('user__email', 'achievement__name')

# ------------ Achievement ------------
@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'rule', 'threshold')
    search_fields = ('code', 'name')

# ------------ Player History ------------
@admin.register(PlayerHistory)
class PlayerHistoryAdmin(admin.ModelAdmin):
    search_fields = ('user__email', 'quiz__title')
    autocomplete_fields = ['user', 'quiz']
