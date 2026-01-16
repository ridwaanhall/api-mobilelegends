from django.urls import path
from django.conf import settings

from . import views


urlpatterns = []

# Add other API endpoints only if available
if settings.IS_AVAILABLE:
    urlpatterns.extend([
        path('academy/version/', views.VersionView.as_view(), name='academy_version'),
        
        path('academy/heroes/', views.HeroesView.as_view(), name='academy_heroes'),
        path('academy/heroes/<int:hero_id>/stats/', views.HeroStatsView.as_view(), name='academy_hero_stats'),
        
        path('academy/roles/', views.RolesView.as_view(), name='academy_roles'),
        
        path('academy/equipment/', views.EquipmentView.as_view(), name='academy_equipment'),
        path('academy/equipment-details/', views.EquipmentDetailsView.as_view(), name='academy_equipment_details'), # items, builds
        path('academy/spells/', views.SpellsView.as_view(), name='academy_spells'),
        path('academy/emblems/', views.EmblemsView.as_view(), name='academy_emblems'),
        
        path('academy/recommended/', views.RecommendedView.as_view(), name='academy_recommended'),
        path('academy/recommended/<int:recommended_id>/', views.RecommendedDetailView.as_view(), name='academy_recommended_detail'),
        
        path('academy/guide/', views.GuideView.as_view(), name='academy_guide'),
    ])