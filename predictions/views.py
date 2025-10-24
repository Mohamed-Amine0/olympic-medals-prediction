from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import OlympicGame, Athlete, Country, Medal, CountryPrediction


def home(request):
    """
    Vue principale affichant les statistiques globales.
    """
    context = {
        'total_games': OlympicGame.objects.count(),
        'total_athletes': Athlete.objects.count(),
        'total_countries': Country.objects.count(),
        'total_medals': Medal.objects.count(),
        'top_countries': Country.objects.all()[:10],
        'recent_games': OlympicGame.objects.all()[:5],
    }
    return render(request, 'predictions/home.html', context)


def countries_list(request):
    """
    Vue listant tous les pays avec leurs statistiques.
    """
    countries = Country.objects.all()
    context = {
        'countries': countries,
    }
    return render(request, 'predictions/countries_list.html', context)


def country_detail(request, country_id):
    """
    Vue détaillée d'un pays avec ses médailles.
    """
    country = get_object_or_404(Country, id=country_id)
    medals = Medal.objects.filter(country=country).select_related('game', 'athlete')[:50]
    
    # Statistiques par discipline
    medals_by_discipline = Medal.objects.filter(country=country).values('discipline_title').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    context = {
        'country': country,
        'medals': medals,
        'medals_by_discipline': medals_by_discipline,
    }
    return render(request, 'predictions/country_detail.html', context)


def games_list(request):
    """
    Vue listant tous les jeux olympiques.
    """
    games = OlympicGame.objects.all()
    context = {
        'games': games,
    }
    return render(request, 'predictions/games_list.html', context)


def game_detail(request, game_id):
    """
    Vue détaillée d'un jeu olympique avec les médailles.
    """
    game = get_object_or_404(OlympicGame, id=game_id)
    medals = Medal.objects.filter(game=game).select_related('country', 'athlete')[:50]
    
    # Top 10 pays pour ce jeu
    top_countries = Medal.objects.filter(game=game).values(
        'country__country_name', 'country__id'
    ).annotate(
        medal_count=Count('id')
    ).order_by('-medal_count')[:10]
    
    context = {
        'game': game,
        'medals': medals,
        'top_countries': top_countries,
    }
    return render(request, 'predictions/game_detail.html', context)


def athletes_list(request):
    """
    Vue listant les athlètes.
    """
    athletes = Athlete.objects.all()[:100]  # Limité à 100 pour performance
    context = {
        'athletes': athletes,
    }
    return render(request, 'predictions/athletes_list.html', context)


def predictions_list(request):
    """
    Vue affichant les prédictions pour les prochains jeux.
    """
    predictions = CountryPrediction.objects.all().select_related('country')
    context = {
        'predictions': predictions,
    }
    return render(request, 'predictions/predictions_list.html', context)
