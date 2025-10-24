"""
Modèles Django pour la prédiction des médailles olympiques.

Ce fichier contient les modèles de données basés sur l'analyse des fichiers sources :
- olympic_athletes.json : Données des athlètes olympiques
- olympic_hosts.xml : Données des jeux olympiques (hôtes)
- olympic_medals.xlsx : Données des médailles
- olympic_results.html : Données des résultats

Colonnes pertinentes sélectionnées pour la prédiction :
1. Country (pays) - Facteur clé : historique des médailles par pays
2. Discipline - Type de sport influence le nombre de médailles
3. Game Year/Season - Tendances temporelles et saison (été/hiver)
4. Athlete participation count - Nombre de participations (expérience)
5. Medal type - Pour l'entraînement du modèle
"""

from django.db import models


class OlympicGame(models.Model):
    """
    Modèle représentant un jeu olympique.
    Source: olympic_hosts.xml
    """
    game_slug = models.CharField(max_length=100, unique=True)
    game_name = models.CharField(max_length=200)
    game_year = models.IntegerField()
    game_season = models.CharField(max_length=20)  # Summer ou Winter
    game_location = models.CharField(max_length=200)
    game_start_date = models.DateTimeField()
    game_end_date = models.DateTimeField()
    
    class Meta:
        ordering = ['-game_year']
    
    def __str__(self):
        return f"{self.game_name} ({self.game_year})"


class Athlete(models.Model):
    """
    Modèle représentant un athlète olympique.
    Source: olympic_athletes.json
    Colonnes pertinentes: athlete_full_name, games_participations, athlete_year_birth
    """
    athlete_full_name = models.CharField(max_length=200)
    athlete_url = models.URLField(max_length=500, unique=True)
    athlete_year_birth = models.IntegerField(null=True, blank=True)
    games_participations = models.IntegerField(default=1)  # Nombre de participations - indicateur d'expérience
    first_game = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['athlete_full_name']
    
    def __str__(self):
        return self.athlete_full_name


class Country(models.Model):
    """
    Modèle représentant un pays participant aux JO.
    Agrégation des données de médailles par pays.
    """
    country_name = models.CharField(max_length=200, unique=True)
    country_code = models.CharField(max_length=10)
    country_3_letter_code = models.CharField(max_length=3)
    
    # Statistiques pour la prédiction
    total_gold_medals = models.IntegerField(default=0)
    total_silver_medals = models.IntegerField(default=0)
    total_bronze_medals = models.IntegerField(default=0)
    total_medals = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-total_medals']
        verbose_name_plural = "Countries"
    
    def __str__(self):
        return self.country_name


class Medal(models.Model):
    """
    Modèle représentant une médaille olympique.
    Source: olympic_medals.xlsx
    Colonnes pertinentes: discipline_title, slug_game, medal_type, country_name, athlete_full_name
    """
    MEDAL_CHOICES = [
        ('GOLD', 'Or'),
        ('SILVER', 'Argent'),
        ('BRONZE', 'Bronze'),
    ]
    
    discipline_title = models.CharField(max_length=200)  # Sport - facteur clé pour prédiction
    slug_game = models.CharField(max_length=100)  # Référence au jeu olympique
    event_title = models.CharField(max_length=300)
    event_gender = models.CharField(max_length=20)
    medal_type = models.CharField(max_length=10, choices=MEDAL_CHOICES)  # Type de médaille - variable cible
    participant_type = models.CharField(max_length=50)
    participant_title = models.CharField(max_length=200, null=True, blank=True)
    
    # Relations
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    game = models.ForeignKey(OlympicGame, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return f"{self.medal_type} - {self.discipline_title} - {self.country.country_name}"


class CountryPrediction(models.Model):
    """
    Modèle pour stocker les prédictions de médailles par pays.
    Résultats du modèle de machine learning.
    """
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    predicted_game = models.CharField(max_length=100)  # Jeu olympique futur
    predicted_gold = models.IntegerField(default=0)
    predicted_silver = models.IntegerField(default=0)
    predicted_bronze = models.IntegerField(default=0)
    predicted_total = models.IntegerField(default=0)
    confidence_score = models.FloatField(default=0.0)  # Score de confiance du modèle
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-predicted_total']
    
    def __str__(self):
        return f"Prédiction pour {self.country.country_name} - {self.predicted_game}"
