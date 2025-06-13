from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls')),

    # Seu override primeiro
    path('accounts/', include('accounts.urls')),

    # O do Django vem depois
    path('accounts/', include('django.contrib.auth.urls')),

    path('', RedirectView.as_view(pattern_name='quiz_list', permanent=False)),
]
