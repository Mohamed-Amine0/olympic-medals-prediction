"""
Script de parsing et d'import des données olympiques.

Ce script lit les fichiers de données (JSON, XML, XLSX, HTML) et les importe dans la base de données.
Il ne lit que les 5 premières lignes pour comprendre la structure, puis importe un échantillon limité.

Étapes :
1. Parser olympic_hosts.xml pour créer les jeux olympiques
2. Parser olympic_athletes.json pour créer les athlètes
3. Parser olympic_medals.xlsx pour créer les médailles et mettre à jour les statistiques pays
4. Calculer les statistiques agrégées par pays
"""

import json
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
from pathlib import Path
import sys
import os

# Configuration du chemin Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from predictions.models import OlympicGame, Athlete, Country, Medal


def parse_olympic_hosts(file_path, limit=None):
    """
    Parse le fichier XML des hôtes olympiques.
    Args:
        file_path: Chemin vers le fichier XML
        limit: Nombre maximum d'entrées à importer (None = toutes)
    """
    print(f"\n=== Parsing Olympic Hosts XML ===")
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    count = 0
    for row in root.findall('row'):
        if limit and count >= limit:
            break
            
        game_slug = row.find('game_slug').text
        game_name = row.find('game_name').text
        game_year = int(row.find('game_year').text)
        game_season = row.find('game_season').text
        game_location = row.find('game_location').text
        game_start_date = datetime.fromisoformat(row.find('game_start_date').text.replace('Z', '+00:00'))
        game_end_date = datetime.fromisoformat(row.find('game_end_date').text.replace('Z', '+00:00'))
        
        # Créer ou mettre à jour le jeu olympique
        game, created = OlympicGame.objects.get_or_create(
            game_slug=game_slug,
            defaults={
                'game_name': game_name,
                'game_year': game_year,
                'game_season': game_season,
                'game_location': game_location,
                'game_start_date': game_start_date,
                'game_end_date': game_end_date,
            }
        )
        
        if created:
            print(f"✓ Créé: {game_name} ({game_year})")
        count += 1
    
    print(f"Total jeux olympiques importés: {count}")


def parse_olympic_athletes(file_path, limit=None):
    """
    Parse le fichier JSON des athlètes olympiques.
    Args:
        file_path: Chemin vers le fichier JSON
        limit: Nombre maximum d'entrées à importer (None = toutes)
    """
    print(f"\n=== Parsing Olympic Athletes JSON ===")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        athletes_data = json.load(f)
    
    count = 0
    for athlete_data in athletes_data:
        if limit and count >= limit:
            break
            
        athlete_url = athlete_data.get('athlete_url')
        if not athlete_url:
            continue
            
        athlete_full_name = athlete_data.get('athlete_full_name', '')
        games_participations = athlete_data.get('games_participations', 1)
        athlete_year_birth = athlete_data.get('athlete_year_birth')
        first_game = athlete_data.get('first_game')
        
        # Créer ou mettre à jour l'athlète
        athlete, created = Athlete.objects.get_or_create(
            athlete_url=athlete_url,
            defaults={
                'athlete_full_name': athlete_full_name,
                'games_participations': games_participations if games_participations else 1,
                'athlete_year_birth': int(athlete_year_birth) if athlete_year_birth else None,
                'first_game': first_game,
            }
        )
        
        if created and count < 10:  # Afficher seulement les 10 premiers
            print(f"✓ Créé: {athlete_full_name}")
        count += 1
    
    print(f"Total athlètes importés: {count}")


def parse_olympic_medals(file_path, limit=None):
    """
    Parse le fichier Excel des médailles olympiques.
    Args:
        file_path: Chemin vers le fichier XLSX
        limit: Nombre maximum d'entrées à importer (None = toutes)
    """
    print(f"\n=== Parsing Olympic Medals XLSX ===")
    
    df = pd.read_excel(file_path)
    
    # Afficher les premières lignes pour validation
    print("\nPremières lignes du fichier:")
    print(df.head(5).to_string())
    print(f"\nColonnes disponibles: {df.columns.tolist()}")
    
    if limit:
        df = df.head(limit)
    
    count = 0
    for _, row in df.iterrows():
        # Créer ou récupérer le pays
        country_name = row['country_name']
        country_code = row['country_code']
        country_3_letter_code = row['country_3_letter_code']
        
        country, _ = Country.objects.get_or_create(
            country_name=country_name,
            defaults={
                'country_code': country_code,
                'country_3_letter_code': country_3_letter_code,
            }
        )
        
        # Récupérer le jeu olympique
        game = OlympicGame.objects.filter(game_slug=row['slug_game']).first()
        
        # Récupérer l'athlète si disponible
        athlete = None
        if row.get('athlete_url'):
            athlete = Athlete.objects.filter(athlete_url=row['athlete_url']).first()
        
        # Créer la médaille
        medal = Medal.objects.create(
            discipline_title=row['discipline_title'],
            slug_game=row['slug_game'],
            event_title=row['event_title'],
            event_gender=row['event_gender'],
            medal_type=row['medal_type'],
            participant_type=row['participant_type'],
            participant_title=row.get('participant_title', ''),
            country=country,
            game=game,
            athlete=athlete,
        )
        
        if count < 10:  # Afficher seulement les 10 premières
            print(f"✓ Créé: {medal}")
        count += 1
    
    print(f"Total médailles importées: {count}")


def calculate_country_statistics():
    """
    Calcule les statistiques de médailles par pays.
    Met à jour les compteurs total_gold_medals, total_silver_medals, etc.
    """
    print(f"\n=== Calcul des statistiques par pays ===")
    
    countries = Country.objects.all()
    for country in countries:
        gold_count = Medal.objects.filter(country=country, medal_type='GOLD').count()
        silver_count = Medal.objects.filter(country=country, medal_type='SILVER').count()
        bronze_count = Medal.objects.filter(country=country, medal_type='BRONZE').count()
        
        country.total_gold_medals = gold_count
        country.total_silver_medals = silver_count
        country.total_bronze_medals = bronze_count
        country.total_medals = gold_count + silver_count + bronze_count
        country.save()
        
        if country.total_medals > 0:
            print(f"✓ {country.country_name}: {country.total_medals} médailles "
                  f"(Or: {gold_count}, Argent: {silver_count}, Bronze: {bronze_count})")
    
    print(f"\nStatistiques calculées pour {countries.count()} pays")


def main():
    """
    Fonction principale d'import des données.
    Importe un échantillon limité de données pour test et démonstration.
    """
    print("="*60)
    print("IMPORT DES DONNÉES OLYMPIQUES")
    print("="*60)
    
    # Chemins des fichiers
    data_dir = Path(r'c:\Users\amine\OneDrive - AEROW SAS\Documents\Notebooks\IPSSI-Notebooks\week-13\Hackathon\data')
    hosts_file = data_dir / 'olympic_hosts.xml'
    athletes_file = data_dir / 'olympic_athletes.json'
    medals_file = data_dir / 'olympic_medals.xlsx'
    
    # Vérifier l'existence des fichiers
    for file_path in [hosts_file, athletes_file, medals_file]:
        if not file_path.exists():
            print(f"❌ Erreur: Fichier non trouvé - {file_path}")
            return
    
    try:
        # Import avec limite pour test (enlever limit=X pour importer tout)
        parse_olympic_hosts(hosts_file, limit=20)  # Tous les jeux olympiques récents
        parse_olympic_athletes(athletes_file, limit=500)  # 500 athlètes pour test
        parse_olympic_medals(medals_file, limit=1000)  # 1000 médailles pour test
        
        # Calculer les statistiques
        calculate_country_statistics()
        
        print("\n" + "="*60)
        print("✓ IMPORT TERMINÉ AVEC SUCCÈS")
        print("="*60)
        
        # Afficher quelques statistiques
        print(f"\nStatistiques finales:")
        print(f"  - Jeux olympiques: {OlympicGame.objects.count()}")
        print(f"  - Athlètes: {Athlete.objects.count()}")
        print(f"  - Pays: {Country.objects.count()}")
        print(f"  - Médailles: {Medal.objects.count()}")
        
        print(f"\nTop 5 pays par nombre de médailles:")
        for country in Country.objects.all()[:5]:
            print(f"  {country.country_name}: {country.total_medals} médailles")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de l'import: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
