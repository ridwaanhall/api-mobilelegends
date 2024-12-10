from django.urls import path
from . import views

urlpatterns = [
    path('rank/', views.rank, name='rank'),
]