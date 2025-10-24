"""
Serializers pour l'API REST de Olympic Medals Prediction.
Convertit les modèles Django en JSON pour l'API.
"""

from rest_framework import serializers
from .models import OlympicGame, Athlete, Country, Medal, CountryPrediction


class OlympicGameSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle OlympicGame."""
    
    class Meta:
        model = OlympicGame
        fields = [
            'id', 'game_slug', 'game_name', 'game_year', 
            'game_season', 'game_location', 'game_start_date', 
            'game_end_date'
        ]


class AthleteSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Athlete."""
    
    class Meta:
        model = Athlete
        fields = [
            'id', 'athlete_full_name', 'athlete_url', 
            'athlete_year_birth', 'games_participations', 'first_game'
        ]


class CountrySerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Country."""
    
    class Meta:
        model = Country
        fields = [
            'id', 'country_name', 'country_code', 'country_3_letter_code',
            'total_gold_medals', 'total_silver_medals', 'total_bronze_medals',
            'total_medals'
        ]


class MedalSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Medal avec relations détaillées."""
    
    country_name = serializers.CharField(source='country.country_name', read_only=True)
    athlete_name = serializers.CharField(source='athlete.athlete_full_name', read_only=True)
    game_name = serializers.CharField(source='game.game_name', read_only=True)
    
    class Meta:
        model = Medal
        fields = [
            'id', 'discipline_title', 'slug_game', 'event_title',
            'event_gender', 'medal_type', 'participant_type',
            'participant_title', 'country', 'country_name',
            'athlete', 'athlete_name', 'game', 'game_name'
        ]


class CountryPredictionSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle CountryPrediction."""
    
    country_name = serializers.CharField(source='country.country_name', read_only=True)
    
    class Meta:
        model = CountryPrediction
        fields = [
            'id', 'country', 'country_name', 'predicted_game',
            'predicted_gold', 'predicted_silver', 'predicted_bronze',
            'predicted_total', 'confidence_score', 'created_at'
        ]


class CountryDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour Country avec ses médailles."""
    
    medals = MedalSerializer(many=True, read_only=True, source='medal_set')
    
    class Meta:
        model = Country
        fields = [
            'id', 'country_name', 'country_code', 'country_3_letter_code',
            'total_gold_medals', 'total_silver_medals', 'total_bronze_medals',
            'total_medals', 'medals'
        ]


class GameDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour OlympicGame avec ses médailles."""
    
    medals = MedalSerializer(many=True, read_only=True, source='medal_set')
    
    class Meta:
        model = OlympicGame
        fields = [
            'id', 'game_slug', 'game_name', 'game_year', 
            'game_season', 'game_location', 'game_start_date', 
            'game_end_date', 'medals'
        ]
