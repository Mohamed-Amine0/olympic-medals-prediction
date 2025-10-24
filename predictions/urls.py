"""
URLs pour l'application predictions.
"""
from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('', views.home, name='home'),
    path('countries/', views.countries_list, name='countries_list'),
    path('countries/<int:country_id>/', views.country_detail, name='country_detail'),
    path('games/', views.games_list, name='games_list'),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    path('athletes/', views.athletes_list, name='athletes_list'),
    path('predictions/', views.predictions_list, name='predictions_list'),
]
