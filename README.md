# Olympic Medals Prediction

Projet Django de prédiction des médailles olympiques basé sur l'analyse de données historiques.

## 📸 Démonstration

![Olympic Medals Prediction Demo](https://github.com/Mohamed-Amine0/olympic-medals-prediction/blob/main/demo/screenshot.png?raw=true)

L'application propose une interface intuitive avec :
- 📊 **Dashboard principal** avec statistiques globales (20 Jeux, 75 Pays, 500 Athlètes, 1000 Médailles)
- 🏆 **Top 10 des pays par médailles** avec classement détaillé (Or, Argent, Bronze)
- 🗓️ **Liste des Jeux Olympiques récents** (Beijing 2022, Tokyo 2020, PyeongChang 2018, etc.)
- 📈 **Analyses avancées** des tendances historiques et performances par discipline
- 🤖 **Prédictions intelligentes** basées sur le machine learning
- 👥 **Profils d'athlètes** avec leurs parcours olympiques

## Description

Ce projet est une application web Django qui permet de :
- Visualiser les statistiques des Jeux Olympiques historiques
- Explorer les performances des pays et athlètes
- Analyser les médailles par discipline et par jeu
- Prédire les futures performances olympiques (avec machine learning)

## Architecture

Le projet suit une architecture MVC (Model-View-Controller) Django :
- **Models** : Modèles de données (OlympicGame, Athlete, Country, Medal, CountryPrediction)
- **Views** : Vues pour gérer la logique métier
- **Templates** : Templates HTML stylisés avec Bootstrap 5

## Technologies Utilisées

- **Backend** : Django 5.2.1
- **Database** : SQLite3
- **Frontend** : HTML5, Bootstrap 5.3, Bootstrap Icons
- **Python Libraries** : pandas, openpyxl (pour le parsing des données)

## Structure du Projet

```
olympic-medals-prediction/
├── config/                 # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── predictions/            # Application principale
│   ├── models.py          # Modèles de données
│   ├── views.py           # Vues
│   ├── urls.py            # URLs
│   ├── admin.py           # Configuration admin Django
│   └── templates/         # Templates HTML
│       └── predictions/
│           ├── base.html
│           ├── home.html
│           ├── countries_list.html
│           ├── country_detail.html
│           ├── games_list.html
│           ├── game_detail.html
│           ├── athletes_list.html
│           └── predictions_list.html
├── data/                  # Données sources
│   ├── olympic_athletes.json
│   ├── olympic_hosts.xml
│   ├── olympic_medals.xlsx
│   └── olympic_results.html
├── import_data.py         # Script d'import des données
├── manage.py              # Script de gestion Django
└── db.sqlite3             # Base de données SQLite
```

## Installation

1. Assurez-vous d'avoir Python 3.8+ installé

2. Installez les dépendances (si nécessaire) :
```bash
pip install django pandas openpyxl
```

3. Appliquez les migrations (si ce n'est pas déjà fait) :
```bash
python manage.py migrate
```

4. Importez les données (si ce n'est pas déjà fait) :
```bash
python import_data.py
```

## Utilisation

### Démarrer le Serveur de Développement

```bash
python manage.py runserver
```

L'application sera accessible sur : http://127.0.0.1:8000/

### Pages Disponibles

- **Accueil** : `/` - Statistiques globales et top pays
- **Pays** : `/countries/` - Liste de tous les pays participants
- **Détail Pays** : `/countries/<id>/` - Détails et médailles d'un pays
- **Jeux Olympiques** : `/games/` - Liste des Jeux Olympiques
- **Détail Jeu** : `/games/<id>/` - Détails d'un Jeu Olympique
- **Athlètes** : `/athletes/` - Liste des athlètes
- **Prédictions** : `/predictions/` - Prédictions pour les prochains jeux
- **Admin** : `/admin/` - Interface d'administration Django

### Interface Admin Django

Pour accéder à l'interface d'administration, créez un superutilisateur :

```bash
python manage.py createsuperuser
```

Puis connectez-vous sur http://127.0.0.1:8000/admin/

## Modèles de Données

### OlympicGame
Représente un jeu olympique avec ses informations (année, saison, lieu, dates).

### Athlete
Représente un athlète olympique avec son nom, année de naissance, et nombre de participations.

### Country
Représente un pays participant avec ses statistiques de médailles.

### Medal
Représente une médaille olympique avec sa discipline, type (Or/Argent/Bronze), pays et athlète.

### CountryPrediction
Stocke les prédictions de médailles futures pour les pays.

## Import des Données

Le script `import_data.py` parse les fichiers suivants :
- `olympic_hosts.xml` : Données des Jeux Olympiques
- `olympic_athletes.json` : Données des athlètes
- `olympic_medals.xlsx` : Données des médailles

Les 5 premières lignes de chaque fichier sont analysées pour comprendre la structure avant l'import.

### Commandes d'Import

```bash
# Import avec limite pour test
python import_data.py

# Pour modifier les limites, éditez le fichier import_data.py
# parse_olympic_hosts(hosts_file, limit=20)
# parse_olympic_athletes(athletes_file, limit=500)
# parse_olympic_medals(medals_file, limit=1000)
```

## Colonnes Pertinentes pour la Prédiction

Les colonnes suivantes ont été identifiées comme pertinentes pour le modèle de prédiction :

1. **Country (Pays)** : Historique des médailles par pays
2. **Discipline** : Type de sport influence le nombre de médailles
3. **Game Year/Season** : Tendances temporelles et saison (été/hiver)
4. **Athlete Participation Count** : Expérience de l'athlète
5. **Medal Type** : Variable cible pour l'entraînement du modèle

## Fonctionnalités

### Actuellement Implémentées
- ✅ Visualisation des statistiques globales
- ✅ Liste et détails des pays
- ✅ Liste et détails des Jeux Olympiques
- ✅ Liste des athlètes
- ✅ Analyse des médailles par discipline
- ✅ Interface responsive avec Bootstrap
- ✅ Interface d'administration Django
- ✅ Import automatique des données

### À Développer
- 🔄 Modèle de machine learning pour les prédictions
- 🔄 Génération automatique des prédictions
- 🔄 Graphiques et visualisations avancées
- 🔄 Filtres et recherche avancée
- 🔄 Export des données (CSV, Excel)
- 🔄 API REST pour accès programmatique

## Tests

Pour tester l'application :

```bash
# Vérifier la configuration Django
python manage.py check

# Tester les URLs
python manage.py show_urls  # Si django-extensions installé

# Accéder à l'interface web
python manage.py runserver
```

## Débogage

En cas de problème :

1. Vérifiez que les migrations sont appliquées :
```bash
python manage.py showmigrations
```

2. Vérifiez que les données sont importées :
```bash
python manage.py shell
>>> from predictions.models import *
>>> print(f"Games: {OlympicGame.objects.count()}")
>>> print(f"Countries: {Country.objects.count()}")
>>> print(f"Medals: {Medal.objects.count()}")
```

3. Consultez les logs du serveur de développement

## Contribution

Ce projet a été développé de manière méthodique et rigoureuse en suivant les meilleures pratiques Django.

## Licence

Projet éducatif - IPSSI 2024

## Auteur

Projet réalisé dans le cadre du Hackathon IPSSI - Week 13
