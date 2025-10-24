# Olympic Medals Prediction

Projet de prédiction des médailles olympiques avec architecture moderne React + Django REST API.

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

Application web moderne permettant de :
- Visualiser les statistiques des Jeux Olympiques historiques
- Explorer les performances des pays et athlètes
- Analyser les médailles par discipline et par jeu
- Prédire les futures performances olympiques (avec machine learning)

## Architecture

Le projet suit une architecture moderne découplée :
- **Frontend** : Application React avec Vite, React Router, Bootstrap 5
- **Backend** : API REST Django avec Django REST Framework
- **Database** : SQLite3
- **Communication** : API REST JSON

## Technologies Utilisées

### Backend
- **Django 5.2.1** - Framework web Python
- **Django REST Framework 3.15.2** - API REST
- **django-cors-headers 4.4.0** - Gestion CORS
- **SQLite3** - Base de données
- **pandas 2.3.0** - Manipulation de données
- **openpyxl 3.1.2** - Parsing Excel

### Frontend
- **React 18** - Bibliothèque UI
- **Vite** - Build tool moderne et rapide
- **React Router** - Routing côté client
- **Axios** - Client HTTP pour API
- **Bootstrap 5** - Framework CSS
- **Bootstrap Icons** - Icônes

## Structure du Projet

```
olympic-medals-prediction/
├── frontend/               # Application React
│   ├── src/
│   │   ├── components/    # Composants réutilisables
│   │   ├── pages/         # Pages de l'application
│   │   ├── services/      # Services API
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── config/                # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── predictions/           # Application Django
│   ├── models.py         # Modèles de données
│   ├── views.py          # Vues Django (legacy)
│   ├── api_views.py      # ViewSets API REST
│   ├── serializers.py    # Serializers DRF
│   ├── urls.py           # URLs Django
│   ├── api_urls.py       # URLs API REST
│   └── templates/        # Templates Django (legacy)
├── data/                 # Données sources
│   ├── olympic_athletes.json
│   ├── olympic_hosts.xml
│   ├── olympic_medals.xlsx
│   └── olympic_results.html
├── import_data.py        # Script d'import des données
├── manage.py
└── requirements.txt
```

## Installation

### Prérequis
- Python 3.8+
- Node.js 18+
- npm 9+

### Backend Django

1. Installez les dépendances Python :
```bash
pip install -r requirements.txt
```

2. Appliquez les migrations :
```bash
python manage.py migrate
```

3. Importez les données :
```bash
python import_data.py
```

4. Démarrez le serveur Django :
```bash
python manage.py runserver
```

Le backend API sera accessible sur : http://localhost:8000/api/

### Frontend React

1. Naviguez vers le dossier frontend :
```bash
cd frontend
```

2. Installez les dépendances :
```bash
npm install
```

3. Créez le fichier .env :
```bash
cp .env.example .env
```

4. Démarrez le serveur de développement :
```bash
npm run dev
```

L'application React sera accessible sur : http://localhost:5173/

## Endpoints API

### Statistiques
- `GET /api/stats/overview/` - Statistiques globales

### Pays
- `GET /api/countries/` - Liste des pays
- `GET /api/countries/{id}/` - Détails d'un pays
- `GET /api/countries/top/` - Top 10 pays

### Jeux Olympiques
- `GET /api/games/` - Liste des jeux
- `GET /api/games/{id}/` - Détails d'un jeu
- `GET /api/games/{id}/top_countries/` - Top pays pour un jeu

### Athlètes
- `GET /api/athletes/` - Liste des athlètes
- `GET /api/athletes/{id}/` - Détails d'un athlète

### Médailles
- `GET /api/medals/` - Liste des médailles
- `GET /api/medals/?country={id}` - Médailles par pays
- `GET /api/medals/?game={id}` - Médailles par jeu

### Prédictions
- `GET /api/predictions/` - Liste des prédictions

Tous les endpoints supportent la pagination avec les paramètres `?page={num}`.

## Fonctionnalités

### Implémentées ✅
- ✅ API REST complète avec Django REST Framework
- ✅ Frontend React moderne avec Vite
- ✅ Routing React Router
- ✅ Communication frontend-backend via Axios
- ✅ Configuration CORS
- ✅ Interface responsive Bootstrap 5
- ✅ Visualisation des statistiques globales
- ✅ Liste et détails des pays
- ✅ Liste et détails des Jeux Olympiques
- ✅ Liste des athlètes
- ✅ Analyse des médailles par discipline
- ✅ Pagination des résultats
- ✅ Gestion des erreurs et chargement

### À Développer 🔄
- 🔄 Modèle de machine learning pour les prédictions
- 🔄 Génération automatique des prédictions
- 🔄 Graphiques et visualisations avancées (Chart.js)
- 🔄 Filtres et recherche avancée
- 🔄 Export des données (CSV, Excel)
- 🔄 Tests unitaires frontend et backend
- 🔄 Déploiement production

## Configuration CORS

Le backend Django est configuré pour accepter les requêtes depuis :
- http://localhost:5173 (Vite dev server)
- http://localhost:3000 (Alternative)

Modifiez `config/settings.py` pour ajouter d'autres origines.

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

## Tests

### Backend
```bash
python manage.py check
python manage.py test
```

### Frontend
```bash
cd frontend
npm run lint
npm run build  # Vérifier que le build fonctionne
```

## Déploiement

### Backend Django
Utilisez gunicorn ou un serveur WSGI :
```bash
pip install gunicorn
gunicorn config.wsgi:application
```

### Frontend React
Build de production :
```bash
cd frontend
npm run build
# Les fichiers seront dans dist/
```

## Contribution

Projet développé avec les meilleures pratiques :
- Architecture découplée frontend/backend
- API REST standardisée
- Code modulaire et réutilisable
- Gestion des erreurs robuste

## Licence

Projet éducatif - IPSSI 2024

## Auteur

Projet réalisé dans le cadre du Hackathon IPSSI - Week 13
