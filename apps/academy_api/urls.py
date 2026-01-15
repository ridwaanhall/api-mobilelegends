from django.urls import path
from django.conf import settings

from . import views


urlpatterns = []

# Add other API endpoints only if available
if settings.IS_AVAILABLE:
    urlpatterns.extend([
        path('academy/hero-list/', views.HeroListView.as_view(), name='academy_hero_list'),
        path('academy/equipment/', views.EquipmentListView.as_view(), name='academy_equipment_list'),
    ])