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
        path('hero-list-new/', views.HeroListNewView.as_view(), name='hero_list_new'),
        path('hero-rank/', views.HeroRankView.as_view(), name='hero_rank'),
        path('hero-position/', views.HeroPositionView.as_view(), name='hero_position'),
        path('hero-detail/<int:hero_id>/', views.HeroDetailView.as_view(), name='hero_detail'),
        path('hero-detail-stats/<int:main_heroid>/', views.HeroDetailStatsView.as_view(), name='hero_detail_stats'),
        path('hero-skill-combo/<int:hero_id>/', views.HeroSkillComboView.as_view(), name='hero_skill_combo'),
        path('hero-rate/<int:main_heroid>/', views.HeroRateView.as_view(), name='hero_rate'),
        path('hero-relation/<int:hero_id>/', views.HeroRelationView.as_view(), name='hero_relation'),
        path('hero-counter/<int:main_heroid>/', views.HeroCounterView.as_view(), name='hero_counter'),
        path('hero-compatibility/<int:main_heroid>/', views.HeroCompatibilityView.as_view(), name='hero_compatibility'),

        path('win-rate/', views.WinRateView.as_view(), name='win_rate'),
    ])