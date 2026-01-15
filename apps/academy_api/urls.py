from django.urls import path
from django.conf import settings

from . import views


urlpatterns = []

# Add other API endpoints only if available
if settings.IS_AVAILABLE:
    urlpatterns.extend([
        path('academy/hero/', views.HeroView.as_view(), name='academy_hero'),
        path('academy/equipment/', views.EquipmentView.as_view(), name='academy_equipment'),
        path('academy/version/', views.VersionView.as_view(), name='academy_version'),
        path('academy/recommended/', views.RecommendedView.as_view(), name='academy_recommended'),
        path('academy/recommended-detail/', views.RecommendedDetailView.as_view(), name='academy_recommended_detail'),
    ])