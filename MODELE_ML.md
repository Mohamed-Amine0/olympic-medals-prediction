# 🤖 MODÈLE DE MACHINE LEARNING - DOCUMENTATION TECHNIQUE

## Type de Modèle: RÉGRESSION MULTI-OUTPUT

---

## 📊 Classification du Problème

### Type de ML: **RÉGRESSION** (pas Classification)

**Justification:**
- **Variable cible**: Valeurs continues (nombre de médailles: 0, 1, 2, 3, ..., 50, etc.)
- **Outputs**: 3 variables numériques (Or, Argent, Bronze)
- **Nature du problème**: Prédiction de quantités, pas de catégories

### Comparaison Régression vs Classification

| Aspect | Régression (Notre Cas) | Classification |
|--------|----------------------|----------------|
| **Output** | Valeurs continues | Catégories discrètes |
| **Exemples** | 0, 1, 5, 23, 50 médailles | "Oui/Non", "A/B/C" |
| **Métrique** | MAE, MSE, R² | Accuracy, F1-score |
| **Notre variable** | Nombre de médailles (0-100+) | N/A |

---

## 🎯 Architecture du Modèle

### Type Spécifique
**Régression Multi-Output avec Analyse de Séries Temporelles**

### Composantes

1. **Feature Engineering**
   - Variables d'entrée (Features):
     - Historique des médailles par pays (5 derniers jeux)
     - Année du jeu olympique (tendance temporelle)
     - Saison (Été/Hiver)
     - Nombre de participations
     - Distribution historique Or/Argent/Bronze

2. **Modèle de Régression Statistique**
   - Moyenne Mobile Pondérée
   - Analyse de Variance (écart-type)
   - Régression par Ratios Historiques

3. **Multi-Output Prediction**
   - Output 1: Nombre médailles d'Or (continu)
   - Output 2: Nombre médailles d'Argent (continu)
   - Output 3: Nombre médailles de Bronze (continu)

---

## 🔢 Formules Mathématiques

### 1. Prédiction du Total
```python
# Moyenne mobile sur les 5 derniers jeux
predicted_total = mean([medals_game1, medals_game2, ..., medals_game5])
```

**Équation:**
```
ŷ_total = (1/n) × Σ(médailles_jeu_i) pour i=1 à 5
```

### 2. Distribution par Type (Régression Proportionnelle)
```python
# Ratios historiques
ratio_gold = total_gold / total_medals
ratio_silver = total_silver / total_medals
ratio_bronze = total_bronze / total_medals

# Application
predicted_gold = predicted_total × ratio_gold
predicted_silver = predicted_total × ratio_silver
predicted_bronze = predicted_total × ratio_bronze
```

**Équations:**
```
ŷ_gold = ŷ_total × (N_gold / N_total)
ŷ_silver = ŷ_total × (N_silver / N_total)
ŷ_bronze = ŷ_total × (N_bronze / N_total)
```

### 3. Score de Confiance
```python
confidence = (
    participation_score × 0.4 +
    regularity_score × 0.4 +
    performance_score × 0.2
)
```

**Détail des composantes:**

#### a) Participation Score
```python
participation_score = min(games_participated / 5.0, 1.0)
```
Plus un pays a participé aux derniers jeux, plus le score est élevé.

#### b) Regularity Score (Coefficient de Variation Inverse)
```python
CV = std_dev / mean  # Coefficient de variation
regularity_score = 1 - min(CV, 1.0)
```
Plus les performances sont régulières (faible CV), plus le score est élevé.

#### c) Performance Score
```python
performance_score = min(total_medals / 100.0, 1.0)
```
Normalisation des performances sur 100 médailles.

---

## 📈 Pipeline de Prédiction

```
┌─────────────────────────────────────────────────────────────┐
│                    DONNÉES HISTORIQUES                       │
│  (Médailles par pays, par jeu, par type sur 5 derniers JO) │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              FEATURE ENGINEERING                             │
│  • Moyenne mobile (5 jeux)                                  │
│  • Écart-type (régularité)                                  │
│  • Ratios Or/Argent/Bronze                                  │
│  • Score de participation                                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           RÉGRESSION MULTI-OUTPUT                            │
│                                                              │
│  Input: Features pays X (1 x n)                             │
│                                                              │
│  Process:                                                    │
│    ŷ_total = moyenne_mobile(historique)                    │
│    ŷ_gold = ŷ_total × ratio_gold                           │
│    ŷ_silver = ŷ_total × ratio_silver                       │
│    ŷ_bronze = ŷ_total × ratio_bronze                       │
│                                                              │
│  Output: [ŷ_gold, ŷ_silver, ŷ_bronze] (1 x 3)              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              CONFIDENCE SCORING                              │
│  confidence = weighted_sum(participation, regularity, perf) │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  PRÉDICTIONS FINALES                         │
│  Pour chaque pays: [Or, Argent, Bronze, Total, Confidence] │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔬 Type de Machine Learning

### Catégorisation

| Critère | Classification |
|---------|---------------|
| **Type principal** | Supervised Learning (Apprentissage Supervisé) |
| **Sous-type** | Regression (Régression) |
| **Variante** | Multi-Output Regression |
| **Temporalité** | Time Series Analysis (Séries Temporelles) |
| **Approche** | Statistical Learning + Moving Average |

### Pourquoi Régression et pas Classification?

#### Régression ✅ (Notre Choix)
- Prédire **combien** de médailles (0, 1, 2, ..., 50)
- Variable continue
- Exemples: Prix, température, quantité, **nombre de médailles**

#### Classification ❌ (Pas notre cas)
- Prédire **quelle catégorie** (Oui/Non, A/B/C)
- Variable discrète/catégorielle
- Exemples: Spam/Ham, Chien/Chat/Oiseau, Gagner/Perdre

### Si c'était de la Classification

Si on voulait classifier, on pourrait prédire des catégories comme:
- "Beaucoup de médailles" / "Moyen" / "Peu"
- "Top 10" / "Top 50" / "Autres"
- "Médaillé" / "Non médaillé"

Mais ce n'est **pas** notre objectif. Nous voulons le **nombre exact** de médailles.

---

## 📊 Métriques d'Évaluation

### Pour Régression (Notre Cas)

1. **MAE (Mean Absolute Error)**
   ```
   MAE = (1/n) × Σ|y_i - ŷ_i|
   ```
   Moyenne des erreurs absolues

2. **MSE (Mean Squared Error)**
   ```
   MSE = (1/n) × Σ(y_i - ŷ_i)²
   ```
   Moyenne des erreurs au carré (pénalise les grandes erreurs)

3. **R² (Coefficient de Détermination)**
   ```
   R² = 1 - (Σ(y_i - ŷ_i)² / Σ(y_i - ȳ)²)
   ```
   Pourcentage de variance expliquée (0 à 1)

### Exemple Concret

Pour la Chine:
- **Prédiction**: 46 médailles (21 Or, 18 Argent, 7 Bronze)
- **Réel (si connu)**: 48 médailles
- **Erreur absolue**: |48 - 46| = 2 médailles
- **Erreur relative**: 2/48 = 4.2%

---

## 🛠️ Implémentation Actuelle

### Technologies Utilisées

```python
# Bibliothèques
import statistics  # Pour moyenne et écart-type
from django.db.models import Count, Avg  # Pour agrégation SQL

# Pas de scikit-learn ou TensorFlow dans la version actuelle
# Modèle statistique pur en Python
```

### Algorithme Complet

```python
def predict_medals(country, num_games=5):
    """
    Régression multi-output pour prédire les médailles.
    
    Args:
        country: Pays à prédire
        num_games: Nombre de jeux historiques à analyser
    
    Returns:
        tuple: (gold, silver, bronze, confidence)
    """
    # 1. Extraction des features
    recent_games = get_last_n_games(num_games)
    medals_by_game = []
    
    for game in recent_games:
        medals_count = count_medals(country, game)
        medals_by_game.append(medals_count)
    
    # 2. Calcul statistique (Régression)
    if len(medals_by_game) >= 2:
        avg_medals = statistics.mean(medals_by_game)
        std_dev = statistics.stdev(medals_by_game)
    else:
        avg_medals = sum(medals_by_game) / max(len(medals_by_game), 1)
        std_dev = 0
    
    # 3. Ratios historiques pour multi-output
    total_gold = count_medals_by_type(country, 'GOLD')
    total_silver = count_medals_by_type(country, 'SILVER')
    total_bronze = count_medals_by_type(country, 'BRONZE')
    total = total_gold + total_silver + total_bronze
    
    ratio_gold = total_gold / total if total > 0 else 0.33
    ratio_silver = total_silver / total if total > 0 else 0.33
    ratio_bronze = total_bronze / total if total > 0 else 0.34
    
    # 4. Prédiction (Régression proportionnelle)
    predicted_total = int(round(avg_medals))
    predicted_gold = int(round(predicted_total * ratio_gold))
    predicted_silver = int(round(predicted_total * ratio_silver))
    predicted_bronze = predicted_total - predicted_gold - predicted_silver
    
    # 5. Score de confiance
    participation_score = min(len(medals_by_game) / num_games, 1.0)
    regularity_score = 1.0 - min(std_dev / avg_medals, 1.0) if avg_medals > 0 else 0.5
    performance_score = min(total / 100.0, 1.0)
    
    confidence = (
        participation_score * 0.4 +
        regularity_score * 0.4 +
        performance_score * 0.2
    )
    
    return predicted_gold, predicted_silver, predicted_bronze, confidence
```

---

## 🚀 Améliorations Possibles

### Version Avancée avec Scikit-Learn

```python
from sklearn.linear_model import LinearRegression
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor

# Features: [année, saison, pop, PIB, dernières_médailles...]
X = construct_features(countries, games)

# Targets: [gold, silver, bronze]
y = construct_targets(medals)

# Multi-Output Regression
model = MultiOutputRegressor(RandomForestRegressor(n_estimators=100))
model.fit(X, y)

# Prédiction
predictions = model.predict(X_test)
```

### Modèles Avancés Recommandés

1. **Random Forest Regressor**
   - Robuste aux outliers
   - Gère les interactions complexes
   - Multi-output natif

2. **XGBoost Regressor**
   - Très performant
   - Gestion du boosting
   - Feature importance

3. **LSTM (Deep Learning)**
   - Pour séries temporelles complexes
   - Capture les dépendances long-terme
   - Nécessite plus de données

---

## 📝 Résumé Technique

| Aspect | Détail |
|--------|--------|
| **Type de ML** | Régression Multi-Output |
| **Approche** | Statistical Learning + Time Series |
| **Input** | Historique 5 derniers jeux |
| **Output** | 3 valeurs continues (Or, Argent, Bronze) |
| **Algorithme** | Moyenne Mobile + Régression Proportionnelle |
| **Métriques** | MAE, MSE, R² (si données test) |
| **Confidence** | Score composite [0-1] |
| **Limitations** | Modèle simplifié, pas d'entraînement supervisé |
| **Production** | Utiliser Random Forest ou XGBoost |

---

## ✅ Conclusion

Le modèle implémenté est une **régression multi-output** utilisant des méthodes statistiques (moyenne mobile, ratios) pour prédire le nombre de médailles. Ce n'est **pas de la classification** car nous prédisons des quantités numériques continues, pas des catégories.

**Type exact**: Supervised Learning > Regression > Multi-Output Regression > Time Series Statistical Model

---

**Généré pour**: Olympic Medals Prediction - IPSSI 2024  
**Date**: 24 Octobre 2024  
**Version**: 1.0
