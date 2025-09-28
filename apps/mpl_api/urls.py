from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('mplid/', views.MPLIDApiListAPIView.as_view(), name='mplid-api-list'),
]

if settings.IS_AVAILABLE:
    urlpatterns.extend([

        path('mplid/standings/', views.MPLIDStandingsAPIView.as_view(), name='mplid-standings'),
        path('mplid/teams/', views.MPLIDTeamAPIView.as_view(), name='mplid-teams'),
        path('mplid/teams/<str:team_id>/', views.MPLIDTeamDetailAPIView.as_view(), name='mplid-team-detail'),
        path('mplid/transfers/', views.MPLIDTransferAPIView.as_view(), name='mplid-transfers'),
        
        path('mplid/team-stats/', views.MPLIDTeamStatsAPIView.as_view(), name='mplid-team-stats'),
        path('mplid/player-stats/', views.MPLIDPlayerStatsAPIView.as_view(), name='mplid-player-stats'),
        path('mplid/hero-stats/', views.MPLIDHeroStatsAPIView.as_view(), name='mplid-hero-stats'),
        path('mplid/hero-pools/', views.MPLIDHeroPoolsAPIView.as_view(), name='mplid-hero-pools'),
        path('mplid/player-pools/', views.MPLIDPlayerPoolsAPIView.as_view(), name='mplid-player-pools'),
        path('mplid/standings-mvp/', views.MPLIDStandingsMVPAPIView.as_view(), name='mplid-standings-mvp'),
        
        # Schedule endpoints
        path('mplid/schedule/', views.MPLIDScheduleAPIView.as_view(), name='mplid-schedule'),
        path('mplid/schedule/week/', views.MPLIDScheduleAllWeeksAPIView.as_view(), name='mplid-schedule-weeks'),
        path('mplid/schedule/week/<int:week_number>/', views.MPLIDScheduleWeekAPIView.as_view(), name='mplid-schedule-week'),
    ])