# Olympic Medals Prediction - Frontend React

Application React moderne pour visualiser et explorer les données des médailles olympiques.

## Technologies Utilisées

- **React 18** - Bibliothèque UI
- **Vite** - Build tool rapide
- **React Router** - Routing
- **Axios** - Client HTTP
- **Bootstrap 5** - Framework CSS
- **Bootstrap Icons** - Icônes

## Installation

```bash
# Installer les dépendances
npm install

# Créer le fichier .env
cp .env.example .env
```

## Configuration

Modifier le fichier `.env` pour configurer l'URL de l'API backend :

```
VITE_API_URL=http://localhost:8000/api
```

## Développement

```bash
# Démarrer le serveur de développement
npm run dev

# L'application sera accessible sur http://localhost:5173
```

## Fonctionnalités

### Pages Principales

1. **Accueil** - Dashboard avec statistiques globales et top pays
2. **Pays** - Liste des pays participants avec leurs médailles
3. **Détails Pays** - Statistiques détaillées d'un pays
4. **Jeux Olympiques** - Liste de tous les jeux olympiques
5. **Détails Jeu** - Informations et classement d'un jeu
6. **Athlètes** - Liste des athlètes olympiques
7. **Prédictions** - Prédictions ML des futures médailles
