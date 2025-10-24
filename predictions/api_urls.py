"""
URL configuration pour l'API REST.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    OlympicGameViewSet, AthleteViewSet, CountryViewSet,
    MedalViewSet, CountryPredictionViewSet, StatsViewSet
)

# Créer un router et enregistrer les viewsets
router = DefaultRouter()
router.register(r'games', OlympicGameViewSet, basename='game')
router.register(r'athletes', AthleteViewSet, basename='athlete')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'medals', MedalViewSet, basename='medal')
router.register(r'predictions', CountryPredictionViewSet, basename='prediction')
router.register(r'stats', StatsViewSet, basename='stats')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
