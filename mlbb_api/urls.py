from django.urls import path
from . import views

urlpatterns = [
    path('', views.DocsByRidwaanhall, name='root_redirect'),
]