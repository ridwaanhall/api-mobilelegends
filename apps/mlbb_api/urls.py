from django.urls import path
from django.conf import settings

from . import views


urlpatterns = [
    path('', views.MlbbApiEndpoints.as_view(), name='root_redirect'),
]

# Add other API endpoints only if available
if settings.IS_AVAILABLE:
    urlpatterns.extend([
        path('docs/', views.MlbbApiEndpoints.as_view(), name='docs'),

        path('hero-list/', views.HeroListView.as_view(), name='hero_list'),
        path('hero-rank/', views.HeroRankView.as_view(), name='hero_rank'),
        path('hero-position/', views.HeroPositionView.as_view(), name='hero_position'),
        path('hero-detail/<str:hero_identifier>/', views.HeroDetailView.as_view(), name='hero_detail'),
        path('hero-detail-stats/<str:hero_identifier>/', views.HeroDetailStatsView.as_view(), name='hero_detail_stats'),
        path('hero-skill-combo/<str:hero_identifier>/', views.HeroSkillComboView.as_view(), name='hero_skill_combo'),
        path('hero-rate/<str:hero_identifier>/', views.HeroRateView.as_view(), name='hero_rate'),
        path('hero-relation/<str:hero_identifier>/', views.HeroRelationView.as_view(), name='hero_relation'),
        path('hero-counter/<str:hero_identifier>/', views.HeroCounterView.as_view(), name='hero_counter'),
        path('hero-compatibility/<str:hero_identifier>/', views.HeroCompatibilityView.as_view(), name='hero_compatibility'),

        path('win-rate/', views.WinRateView.as_view(), name='win_rate'),
    ])