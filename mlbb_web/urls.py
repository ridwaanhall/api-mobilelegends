from django.urls import path
from . import views

urlpatterns = [
    path('', views.simple_view, name='simple_view'),
    path('hero-rank/', views.hero_rank_web, name='hero_rank_web'),
    path('hero-position/', views.hero_position_web, name='hero_position_web'),
]