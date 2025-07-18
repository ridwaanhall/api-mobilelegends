from django.urls import path
from .views import MPLStandingsIdAPIView

urlpatterns = [
    path("id-mpl/standings/", MPLStandingsIdAPIView.as_view(), name="id-mpl-standings"),
]