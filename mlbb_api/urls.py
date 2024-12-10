from django.urls import path
from . import views

urlpatterns = [
    path('hero-rank/', views.hero_rank, name='hero-rank'),
    path('hero-position/', views.hero_position, name='hero-position'),
]