from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.simple_view, name='simple_view'),
]

# Add other web endpoints only if available
if settings.IS_AVAILABLE:
    urlpatterns.extend([
        path('hero-list/', views.hero_list_web, name='hero_list_web'),
        path('hero-rank/', views.hero_rank_web, name='hero_rank_web'),
        path('hero-position/', views.hero_position_web, name='hero_position_web'),
        path('hero-detail/<int:hero_id>/', views.hero_detail_web, name='hero_detail_web'),
    ])