from django.urls import path
from .views import MPLStandingsAPIView

urlpatterns = [
    path("standings/", MPLStandingsAPIView.as_view(), name="mpl-standings"),
]