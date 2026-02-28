from django.urls import path
from django.conf import settings

from . import views


urlpatterns = []

# Add other API endpoints only if available
if settings.IS_AVAILABLE:
    urlpatterns.extend([
        path('academy/version/', views.VersionView.as_view(), name='academy_version'),
        
        path('academy/heroes/', views.HeroesView.as_view(), name='academy_heroes'),
        
        path('academy/roles/', views.RolesView.as_view(), name='academy_roles'),
        
        path('academy/equipment/', views.EquipmentView.as_view(), name='academy_equipment'),
        path('academy/equipment-details/', views.EquipmentDetailsView.as_view(), name='academy_equipment_details'), # items, builds
        path('academy/spells/', views.SpellsView.as_view(), name='academy_spells'),
        path('academy/emblems/', views.EmblemsView.as_view(), name='academy_emblems'),
        
        path('academy/recommended/', views.RecommendedView.as_view(), name='academy_recommended'),
        path('academy/recommended/<int:recommended_id>/', views.RecommendedDetailView.as_view(), name='academy_recommended_detail'),
        
        path('academy/guide/', views.GuideView.as_view(), name='academy_guide'),
        path('academy/guide/<int:hero_id>/stats/', views.HeroGuideStatsView.as_view(), name='academy_hero_guide_stats'),
        path('academy/guide/<int:hero_id>/lane/', views.HeroGuideLaneView.as_view(), name='academy_hero_guide_lane'),
        path('academy/guide/<int:hero_id>/time-win-rate/<int:lane_id>/', views.HeroGuideTimeWinRateView.as_view(), name='academy_hero_guide_time_win_rate'),
        path('academy/guide/<int:hero_id>/builds/', views.HeroGuideBuildsView.as_view(), name='academy_hero_guide_builds'),
        path('academy/guide/<int:hero_id>/counters/', views.HeroGuideCountersView.as_view(), name='academy_hero_guide_counters'),
        path('academy/guide/<int:hero_id>/teammates/', views.HeroGuideTeammatesView.as_view(), name='academy_hero_guide_teammates'),
        path('academy/guide/<int:hero_id>/trends/', views.HeroGuideTrendsView.as_view(), name='academy_hero_guide_trends'),
        path('academy/guide/<int:hero_id>/recommended/', views.RecommendedHeroView.as_view(), name='academy_hero_guide_recommended'),
        
        path('academy/hero-ratings/', views.HeroRatingsView.as_view(), name='academy_hero_ratings'),
        path('academy/hero-ratings/<str:subject>/', views.HeroRatingsSubjectView.as_view(), name='academy_hero_ratings_subject'),
    ])