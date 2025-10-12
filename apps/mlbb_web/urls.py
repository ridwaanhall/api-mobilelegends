from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('favicon.ico', views.favicon_view, name='favicon'),
]

# Add other web endpoints only if available
if settings.IS_AVAILABLE:
    urlpatterns.extend([
        path('hero-list/', views.MLBBWebViews.hero_list_web, name='hero_list_web'),
        path('hero-rank/', views.MLBBWebViews.hero_rank_web, name='hero_rank_web'),
        path('hero-position/', views.MLBBWebViews.hero_position_web, name='hero_position_web'),
        path('hero-detail/<int:hero_id>/', views.MLBBWebViews.hero_detail_web, name='hero_detail_web'),
        path('refresh-heroes/', views.MLBBWebViews.refresh_hero_cache_view, name='refresh_hero_cache'),
    ])