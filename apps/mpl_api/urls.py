from django.urls import path
from .views import MPLIDStandingsAPIView, MPLIDTeamAPIView, MPLIDTeamDetailAPIView

urlpatterns = [
    path('mplid/standings/', MPLIDStandingsAPIView.as_view(), name='mplid-standings'),
    path('mplid/teams/', MPLIDTeamAPIView.as_view(), name='mplid-teams'),
    path('mplid/teams/<str:team_id>/', MPLIDTeamDetailAPIView.as_view(), name='mplid-team-detail'),
]