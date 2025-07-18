from django.urls import path
from . import views

urlpatterns = [
    path('mplid/standings/', views.MPLIDStandingsAPIView.as_view(), name='mplid-standings'),
    path('mplid/teams/', views.MPLIDTeamAPIView.as_view(), name='mplid-teams'),
    path('mplid/teams/<str:team_id>/', views.MPLIDTeamDetailAPIView.as_view(), name='mplid-team-detail'),
    path('mplid/transfers/', views.MPLIDTransferAPIView.as_view(), name='mplid-transfers'),
]