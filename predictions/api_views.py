"""
API ViewSets pour l'API REST de Olympic Medals Prediction.
Fournit les endpoints CRUD pour tous les modèles.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import OlympicGame, Athlete, Country, Medal, CountryPrediction
from .serializers import (
    OlympicGameSerializer, AthleteSerializer, CountrySerializer,
    MedalSerializer, CountryPredictionSerializer,
    CountryDetailSerializer, GameDetailSerializer
)


class OlympicGameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les Jeux Olympiques.
    Liste tous les jeux olympiques et permet de récupérer les détails d'un jeu.
    """
    queryset = OlympicGame.objects.all()
    serializer_class = OlympicGameSerializer
    
    def retrieve(self, request, pk=None):
        """Récupère les détails d'un jeu avec ses médailles."""
        game = self.get_object()
        serializer = GameDetailSerializer(game, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def top_countries(self, request, pk=None):
        """Retourne le top 10 des pays pour ce jeu olympique."""
        game = self.get_object()
        top_countries = Medal.objects.filter(game=game).values(
            'country__country_name', 'country__id'
        ).annotate(
            medal_count=Count('id')
        ).order_by('-medal_count')[:10]
        
        return Response(top_countries)


class AthleteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les Athlètes.
    Liste tous les athlètes olympiques.
    """
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les Pays.
    Liste tous les pays avec leurs statistiques de médailles.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    
    def retrieve(self, request, pk=None):
        """Récupère les détails d'un pays avec ses médailles (limitées)."""
        country = self.get_object()
        serializer = CountrySerializer(country, context={'request': request})
        
        # Récupérer les 50 premières médailles
        medals = Medal.objects.filter(country=country).select_related(
            'game', 'athlete'
        )[:50]
        
        # Statistiques par discipline
        medals_by_discipline = Medal.objects.filter(country=country).values(
            'discipline_title'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:10]
        
        data = serializer.data
        data['medals'] = MedalSerializer(medals, many=True).data
        data['medals_by_discipline'] = medals_by_discipline
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def top(self, request):
        """Retourne le top 10 des pays par nombre de médailles."""
        top_countries = Country.objects.all()[:10]
        serializer = self.get_serializer(top_countries, many=True)
        return Response(serializer.data)


class MedalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les Médailles.
    Liste toutes les médailles olympiques.
    """
    queryset = Medal.objects.all().select_related('country', 'athlete', 'game')
    serializer_class = MedalSerializer
    
    def get_queryset(self):
        """Permet de filtrer les médailles par pays, jeu ou discipline."""
        queryset = Medal.objects.all().select_related('country', 'athlete', 'game')
        
        # Filtres optionnels
        country_id = self.request.query_params.get('country', None)
        game_id = self.request.query_params.get('game', None)
        discipline = self.request.query_params.get('discipline', None)
        medal_type = self.request.query_params.get('type', None)
        
        if country_id is not None:
            queryset = queryset.filter(country_id=country_id)
        if game_id is not None:
            queryset = queryset.filter(game_id=game_id)
        if discipline is not None:
            queryset = queryset.filter(discipline_title__icontains=discipline)
        if medal_type is not None:
            queryset = queryset.filter(medal_type=medal_type.upper())
        
        return queryset


class CountryPredictionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les Prédictions.
    Liste toutes les prédictions de médailles par pays.
    """
    queryset = CountryPrediction.objects.all().select_related('country')
    serializer_class = CountryPredictionSerializer


class StatsViewSet(viewsets.ViewSet):
    """
    API endpoint pour les statistiques globales.
    """
    
    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Retourne les statistiques globales de l'application."""
        stats = {
            'total_games': OlympicGame.objects.count(),
            'total_athletes': Athlete.objects.count(),
            'total_countries': Country.objects.count(),
            'total_medals': Medal.objects.count(),
            'gold_medals': Medal.objects.filter(medal_type='GOLD').count(),
            'silver_medals': Medal.objects.filter(medal_type='SILVER').count(),
            'bronze_medals': Medal.objects.filter(medal_type='BRONZE').count(),
        }
        return Response(stats)
    
    def list(self, request):
        """Alias pour overview."""
        return self.overview(request)
