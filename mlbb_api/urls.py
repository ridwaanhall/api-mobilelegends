from django.urls import path
from . import views

urlpatterns = [
    path('hero-rank/', views.hero_rank, name='hero_rank'),
    
    path('hero-position/', views.hero_position, name='hero_position'),
    
    path('hero-detail/<int:hero_id>/', views.hero_detail, name='hero_detail'),
    path('hero-detail-stats/<int:main_heroid>/', views.hero_detail_stats, name='hero_detail_stats'),
    path('hero-skill-combo/<int:hero_id>/', views.hero_skill_combo, name='hero_skill_combo'),
    path('hero-rate/<int:main_heroid>/', views.hero_rate, name='hero_rate'),
    path('hero-relation/<int:hero_id>/', views.hero_relation, name='hero_relation'),
    path('hero-counter/<int:main_heroid>/', views.hero_counter, name='hero_counter'),
    path('hero-compatibility/<int:main_heroid>/', views.hero_compatibility, name='hero_compatibility'),
]