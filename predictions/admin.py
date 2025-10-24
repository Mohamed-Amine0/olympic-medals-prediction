from django.contrib import admin
from .models import OlympicGame, Athlete, Country, Medal, CountryPrediction


@admin.register(OlympicGame)
class OlympicGameAdmin(admin.ModelAdmin):
    list_display = ('game_name', 'game_year', 'game_season', 'game_location', 'game_start_date')
    list_filter = ('game_season', 'game_year')
    search_fields = ('game_name', 'game_location')
    ordering = ('-game_year',)


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = ('athlete_full_name', 'athlete_year_birth', 'games_participations', 'first_game')
    list_filter = ('games_participations',)
    search_fields = ('athlete_full_name',)
    ordering = ('athlete_full_name',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_code', 'total_gold_medals', 'total_silver_medals', 'total_bronze_medals', 'total_medals')
    list_filter = ('country_code',)
    search_fields = ('country_name', 'country_code')
    ordering = ('-total_medals',)


@admin.register(Medal)
class MedalAdmin(admin.ModelAdmin):
    list_display = ('discipline_title', 'medal_type', 'country', 'game', 'event_gender')
    list_filter = ('medal_type', 'discipline_title', 'event_gender')
    search_fields = ('discipline_title', 'event_title', 'country__country_name')
    raw_id_fields = ('athlete', 'country', 'game')


@admin.register(CountryPrediction)
class CountryPredictionAdmin(admin.ModelAdmin):
    list_display = ('country', 'predicted_game', 'predicted_total', 'confidence_score', 'created_at')
    list_filter = ('predicted_game', 'created_at')
    search_fields = ('country__country_name',)
    ordering = ('-predicted_total',)
    raw_id_fields = ('country',)
