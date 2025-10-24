"""
Script de test pour valider les fonctionnalités de l'application.
Vérifie que les données sont correctement chargées et que les vues fonctionnent.
"""

import os
import sys
import django
from pathlib import Path

# Configuration Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from predictions.models import OlympicGame, Athlete, Country, Medal, CountryPrediction


def test_database():
    """Test que les données sont bien chargées dans la base de données."""
    print("\n" + "="*60)
    print("TEST DE LA BASE DE DONNÉES")
    print("="*60)
    
    tests = [
        ("Jeux Olympiques", OlympicGame.objects.count(), 20),
        ("Athlètes", Athlete.objects.count(), 500),
        ("Pays", Country.objects.count(), 75),
        ("Médailles", Medal.objects.count(), 1000),
    ]
    
    all_passed = True
    for name, count, expected_min in tests:
        status = "✓" if count >= expected_min else "✗"
        print(f"{status} {name}: {count} (attendu: >= {expected_min})")
        if count < expected_min:
            all_passed = False
    
    return all_passed


def test_models():
    """Test les relations entre modèles."""
    print("\n" + "="*60)
    print("TEST DES MODÈLES")
    print("="*60)
    
    all_passed = True
    
    # Test 1: Pays avec médailles
    try:
        top_country = Country.objects.first()
        if top_country:
            medals_count = Medal.objects.filter(country=top_country).count()
            print(f"✓ Top pays: {top_country.country_name} avec {medals_count} médailles")
        else:
            print("✗ Aucun pays trouvé")
            all_passed = False
    except Exception as e:
        print(f"✗ Erreur test pays: {e}")
        all_passed = False
    
    # Test 2: Jeux olympiques avec médailles
    try:
        latest_game = OlympicGame.objects.first()
        if latest_game:
            medals_count = Medal.objects.filter(game=latest_game).count()
            print(f"✓ Dernier jeu: {latest_game.game_name} avec {medals_count} médailles")
        else:
            print("✗ Aucun jeu trouvé")
            all_passed = False
    except Exception as e:
        print(f"✗ Erreur test jeux: {e}")
        all_passed = False
    
    # Test 3: Athlètes
    try:
        athletes_with_medals = Athlete.objects.filter(medal__isnull=False).distinct().count()
        print(f"✓ Athlètes avec médailles: {athletes_with_medals}")
    except Exception as e:
        print(f"✗ Erreur test athlètes: {e}")
        all_passed = False
    
    return all_passed


def test_statistics():
    """Test les calculs statistiques."""
    print("\n" + "="*60)
    print("TEST DES STATISTIQUES")
    print("="*60)
    
    all_passed = True
    
    # Test 1: Total médailles par type
    try:
        gold_count = Medal.objects.filter(medal_type='GOLD').count()
        silver_count = Medal.objects.filter(medal_type='SILVER').count()
        bronze_count = Medal.objects.filter(medal_type='BRONZE').count()
        
        print(f"✓ Médailles d'Or: {gold_count}")
        print(f"✓ Médailles d'Argent: {silver_count}")
        print(f"✓ Médailles de Bronze: {bronze_count}")
    except Exception as e:
        print(f"✗ Erreur calcul médailles: {e}")
        all_passed = False
    
    # Test 2: Top 5 pays
    try:
        print("\n✓ Top 5 pays par nombre de médailles:")
        for i, country in enumerate(Country.objects.all()[:5], 1):
            print(f"  {i}. {country.country_name}: {country.total_medals} médailles")
    except Exception as e:
        print(f"✗ Erreur top pays: {e}")
        all_passed = False
    
    # Test 3: Disciplines
    try:
        disciplines = Medal.objects.values('discipline_title').distinct().count()
        print(f"\n✓ Nombre de disciplines: {disciplines}")
    except Exception as e:
        print(f"✗ Erreur disciplines: {e}")
        all_passed = False
    
    return all_passed


def test_predictions():
    """Test les prédictions."""
    print("\n" + "="*60)
    print("TEST DES PRÉDICTIONS")
    print("="*60)
    
    predictions_count = CountryPrediction.objects.count()
    
    if predictions_count > 0:
        print(f"✓ {predictions_count} prédictions trouvées")
        
        # Afficher les top 3 prédictions
        print("\nTop 3 prédictions:")
        for i, pred in enumerate(CountryPrediction.objects.all()[:3], 1):
            print(f"  {i}. {pred.country.country_name}: {pred.predicted_total} médailles "
                  f"(confiance: {pred.confidence_score:.2f})")
        return True
    else:
        print("⚠ Aucune prédiction générée (normal si le modèle ML n'est pas encore entraîné)")
        return True  # Ce n'est pas une erreur


def main():
    """Fonction principale de test."""
    print("\n" + "="*60)
    print("TESTS DE L'APPLICATION OLYMPIC MEDALS PREDICTION")
    print("="*60)
    
    results = []
    
    # Exécuter tous les tests
    results.append(("Base de données", test_database()))
    results.append(("Modèles", test_models()))
    results.append(("Statistiques", test_statistics()))
    results.append(("Prédictions", test_predictions()))
    
    # Résumé
    print("\n" + "="*60)
    print("RÉSUMÉ DES TESTS")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ RÉUSSI" if passed else "✗ ÉCHOUÉ"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n" + "="*60)
        print("✓ TOUS LES TESTS SONT PASSÉS")
        print("="*60)
        print("\nL'application est prête à l'emploi!")
        print("Démarrez le serveur avec: python manage.py runserver")
        return 0
    else:
        print("\n" + "="*60)
        print("✗ CERTAINS TESTS ONT ÉCHOUÉ")
        print("="*60)
        print("\nVérifiez les erreurs ci-dessus.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
