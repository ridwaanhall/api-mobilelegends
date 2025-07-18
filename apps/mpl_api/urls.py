from django.urls import path
from . import views

urlpatterns = [
    path("id-mpl/standings/", views.MPLStandingsIdAPIView.as_view(), name="id-mpl-standings"),
    path("id-mpl/teams/", views.MPLTeamIdAPIView.as_view(), name="id-mpl-teams"),
]