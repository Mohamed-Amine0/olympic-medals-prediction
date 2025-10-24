"""
Script de machine learning pour prédire les médailles olympiques.

Ce script utilise un modèle simple basé sur l'historique des performances
pour prédire le nombre de médailles par pays pour les prochains jeux.

Approche :
1. Analyse de l'historique des médailles par pays
2. Calcul de la moyenne mobile et des tendances
3. Prédiction basée sur les performances récentes
4. Score de confiance basé sur la régularité des performances
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from predictions.models import OlympicGame, Country, Medal, CountryPrediction
from django.db.models import Count, Q
import statistics


def calculate_country_statistics(country):
    """
    Calcule les statistiques avancées pour un pays.
    """
    medals = Medal.objects.filter(country=country)
    
    # Comptage par type de médaille
    gold = medals.filter(medal_type='GOLD').count()
    silver = medals.filter(medal_type='SILVER').count()
    bronze = medals.filter(medal_type='BRONZE').count()
    total = gold + silver + bronze
    
    # Médailles par jeu (pour calculer la tendance)
    medals_by_game = []
    games = OlympicGame.objects.all().order_by('-game_year')[:5]  # 5 derniers jeux
    
    for game in games:
        game_medals = medals.filter(game=game).count()
        if game_medals > 0:
            medals_by_game.append(game_medals)
    
    # Calcul de la tendance et de la régularité
    if len(medals_by_game) >= 2:
        avg_medals = statistics.mean(medals_by_game)
        std_dev = statistics.stdev(medals_by_game) if len(medals_by_game) > 2 else 0
    else:
        avg_medals = total / max(len(games), 1)
        std_dev = 0
    
    return {
        'total': total,
        'gold': gold,
        'silver': silver,
        'bronze': bronze,
        'avg_medals': avg_medals,
        'std_dev': std_dev,
        'medals_by_game': medals_by_game,
        'games_count': len(medals_by_game)
    }


def calculate_confidence_score(stats):
    """
    Calcule un score de confiance basé sur :
    - Le nombre de participations historiques
    - La régularité des performances
    - Le nombre total de médailles
    """
    # Plus le pays a participé, plus on est confiant
    participation_score = min(stats['games_count'] / 5.0, 1.0)
    
    # Plus les performances sont régulières, plus on est confiant
    if stats['avg_medals'] > 0 and stats['std_dev'] > 0:
        regularity_score = 1.0 - min(stats['std_dev'] / stats['avg_medals'], 1.0)
    else:
        regularity_score = 0.5
    
    # Plus le pays a de médailles, plus on est confiant
    performance_score = min(stats['total'] / 100.0, 1.0)
    
    # Score combiné (moyenne pondérée)
    confidence = (
        participation_score * 0.4 +
        regularity_score * 0.4 +
        performance_score * 0.2
    )
    
    return round(confidence, 3)


def predict_medal_distribution(stats):
    """
    Prédit la distribution des médailles (or, argent, bronze)
    basée sur les ratios historiques.
    """
    total = stats['total']
    
    if total == 0:
        return 0, 0, 0
    
    # Ratios historiques
    gold_ratio = stats['gold'] / total
    silver_ratio = stats['silver'] / total
    bronze_ratio = stats['bronze'] / total
    
    # Prédiction basée sur la moyenne des derniers jeux
    predicted_total = int(round(stats['avg_medals']))
    
    # Application des ratios
    predicted_gold = int(round(predicted_total * gold_ratio))
    predicted_silver = int(round(predicted_total * silver_ratio))
    predicted_bronze = predicted_total - predicted_gold - predicted_silver
    
    # Ajustement si nécessaire
    if predicted_bronze < 0:
        predicted_bronze = 0
    
    return predicted_gold, predicted_silver, predicted_bronze


def generate_predictions(target_game="Paris 2024 (Futur)", min_medals=1):
    """
    Génère les prédictions pour tous les pays ayant un historique.
    
    Args:
        target_game: Nom du jeu olympique futur à prédire
        min_medals: Nombre minimum de médailles historiques pour faire une prédiction
    """
    print("\n" + "="*60)
    print("GÉNÉRATION DES PRÉDICTIONS")
    print("="*60)
    
    # Supprimer les anciennes prédictions
    old_count = CountryPrediction.objects.count()
    CountryPrediction.objects.all().delete()
    print(f"✓ {old_count} anciennes prédictions supprimées")
    
    # Récupérer tous les pays avec des médailles
    countries = Country.objects.filter(total_medals__gte=min_medals).order_by('-total_medals')
    
    predictions_created = 0
    
    print(f"\nGénération des prédictions pour {countries.count()} pays...")
    print(f"Jeu cible: {target_game}\n")
    
    for country in countries:
        # Calculer les statistiques
        stats = calculate_country_statistics(country)
        
        # Skip si pas assez de données
        if stats['total'] < min_medals:
            continue
        
        # Calculer la prédiction
        predicted_gold, predicted_silver, predicted_bronze = predict_medal_distribution(stats)
        predicted_total = predicted_gold + predicted_silver + predicted_bronze
        
        # Skip si la prédiction est nulle
        if predicted_total == 0:
            continue
        
        # Calculer le score de confiance
        confidence = calculate_confidence_score(stats)
        
        # Créer la prédiction
        prediction = CountryPrediction.objects.create(
            country=country,
            predicted_game=target_game,
            predicted_gold=predicted_gold,
            predicted_silver=predicted_silver,
            predicted_bronze=predicted_bronze,
            predicted_total=predicted_total,
            confidence_score=confidence
        )
        
        predictions_created += 1
        
        # Afficher les 10 premières prédictions
        if predictions_created <= 10:
            print(f"✓ {country.country_name:30} -> {predicted_total:3} médailles "
                  f"(Or:{predicted_gold} Ag:{predicted_silver} Br:{predicted_bronze}) "
                  f"Confiance: {confidence:.2f}")
    
    print(f"\n✓ {predictions_created} prédictions créées avec succès!")
    return predictions_created


def display_predictions_summary():
    """
    Affiche un résumé des prédictions générées.
    """
    print("\n" + "="*60)
    print("RÉSUMÉ DES PRÉDICTIONS")
    print("="*60)
    
    predictions = CountryPrediction.objects.all()
    
    if predictions.count() == 0:
        print("Aucune prédiction disponible.")
        return
    
    print(f"\nTotal de prédictions: {predictions.count()}")
    
    # Top 10 prédictions
    print("\n" + "-"*60)
    print("TOP 10 PRÉDICTIONS POUR LES PROCHAINS JEUX")
    print("-"*60)
    print(f"{'Rang':<6}{'Pays':<30}{'Total':<8}{'Or':<6}{'Ag':<6}{'Br':<6}{'Conf.':<8}")
    print("-"*60)
    
    for i, pred in enumerate(predictions[:10], 1):
        print(f"{i:<6}{pred.country.country_name[:28]:<30}"
              f"{pred.predicted_total:<8}"
              f"{pred.predicted_gold:<6}"
              f"{pred.predicted_silver:<6}"
              f"{pred.predicted_bronze:<6}"
              f"{pred.confidence_score:<8.2f}")
    
    # Statistiques
    total_predicted_medals = sum(p.predicted_total for p in predictions)
    avg_confidence = sum(p.confidence_score for p in predictions) / predictions.count()
    
    print("-"*60)
    print(f"Total médailles prédites: {total_predicted_medals}")
    print(f"Confiance moyenne: {avg_confidence:.2f}")


def main():
    """
    Fonction principale.
    """
    print("\n" + "="*60)
    print("MODÈLE DE PRÉDICTION DES MÉDAILLES OLYMPIQUES")
    print("="*60)
    
    try:
        # Vérifier que les données sont présentes
        medals_count = Medal.objects.count()
        countries_count = Country.objects.count()
        
        print(f"\nDonnées disponibles:")
        print(f"  - Médailles: {medals_count}")
        print(f"  - Pays: {countries_count}")
        
        if medals_count == 0:
            print("\n❌ Erreur: Aucune donnée de médaille trouvée.")
            print("Exécutez d'abord: python import_data.py")
            return 1
        
        # Générer les prédictions
        predictions_count = generate_predictions(
            target_game="Paris 2024 (Futur)",
            min_medals=5  # Au moins 5 médailles historiques
        )
        
        if predictions_count > 0:
            # Afficher le résumé
            display_predictions_summary()
            
            print("\n" + "="*60)
            print("✓ PRÉDICTIONS GÉNÉRÉES AVEC SUCCÈS")
            print("="*60)
            print("\nAccédez aux prédictions sur: http://127.0.0.1:8000/predictions/")
            return 0
        else:
            print("\n❌ Aucune prédiction n'a pu être générée.")
            return 1
            
    except Exception as e:
        print(f"\n❌ Erreur lors de la génération des prédictions: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
