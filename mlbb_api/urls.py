from django.urls import path
from . import views

urlpatterns = [
    path('hero-rank/', views.hero_rank, name='hero_rank'),
    path('hero-position/', views.hero_position, name='hero_position'),
    path('hero-detail/<int:hero_id>/', views.hero_detail, name='hero_detail'),
    path('hero-detail-stats/<int:main_hero_id>/', views.hero_detail_stats, name='hero_detail_stats'),
    path('hero-detail-combos/<int:hero_id>/', views.hero_detail_combos, name='hero_detail_combos'),
]