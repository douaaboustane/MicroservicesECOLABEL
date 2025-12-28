# ⭐ Scoring Service

Service de calcul de score écologique (A-E) utilisant des modèles Machine Learning (Classification + Régression).

## 🎯 Fonctionnalités

- ✅ **Classification** : Prédit directement A-E avec Random Forest Classifier
- ✅ **Régression** : Prédit score 0-100 puis convertit en A-E avec Random Forest Regressor
- ✅ **Hybrid** : Combine les deux méthodes pour meilleure précision
- ✅ **Feature Extraction** : Extraction automatique depuis données LCA et NLP
- ✅ **API REST** : FastAPI avec Swagger UI

---

## 🚀 Installation & Démarrage

### Option 1 : Docker (Recommandé)

```bash
# Depuis la racine du projet
docker-compose up -d scoring-service

# L'API sera disponible sur http://localhost:8005
```

### Option 2 : Local

```bash
cd backend/scoring-service
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8005 --reload
```

---

## 📖 API Documentation

### Swagger UI

Une fois le service démarré, accédez à la documentation interactive :

👉 **http://localhost:8005/docs**

---

## 🔥 Exemple d'Utilisation

### Calcul de score (méthode hybride)

```bash
curl -X POST "http://localhost:8005/score/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "lca_data": {
      "co2_kg": 2.5,
      "water_liters": 500.0,
      "energy_mj": 8.0
    },
    "nlp_data": {
      "ingredients": ["farine de blé", "eau", "sel"],
      "allergens": ["gluten"],
      "labels": ["bio"],
      "has_bio_label": true,
      "has_recyclable_packaging": true,
      "has_palm_oil": false
    },
    "method": "hybrid"
  }'
```

### Résultat

```json
{
  "score_letter": "B",
  "score_numeric": 72.5,
  "confidence": 0.85,
  "method": "hybrid_consensus",
  "probabilities": {
    "A": 0.15,
    "B": 0.70,
    "C": 0.10,
    "D": 0.04,
    "E": 0.01
  },
  "details": {
    "method_used": "hybrid_consensus",
    "probabilities": {...}
  }
}
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│ FastAPI (Port 8005)                 │
│  • POST /score/calculate            │
│  • GET /score/models/info           │
│  • GET /health                      │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ ScoringService                      │
│  • Feature Extraction               │
│  • Model Prediction                 │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ ScoringModels                       │
│  • RandomForestClassifier           │
│  • RandomForestRegressor            │
│  • Hybrid Approach                  │
└─────────────────────────────────────┘
```

---

## 🤖 Modèles ML

### Classification (Random Forest Classifier)

- **Input** : Features extraites (LCA + NLP)
- **Output** : Classe directe (A, B, C, D, E)
- **Avantages** : Prédiction directe, probabilités disponibles

### Régression (Random Forest Regressor)

- **Input** : Features extraites (LCA + NLP)
- **Output** : Score numérique (0-100) → converti en A-E
- **Avantages** : Plus de granularité, meilleure pour valeurs intermédiaires

### Hybrid (Recommandé)

- Combine classification et régression
- Consensus si les deux sont d'accord
- Utilise celui avec plus de confiance en cas de désaccord

---

## 📊 Features Extraites

Le service extrait automatiquement 24 features :

### Impacts LCA (5)
- `co2_kg` : Émissions CO2
- `water_liters` : Consommation d'eau
- `energy_mj` : Énergie
- `acidification` : Acidification
- `eutrophisation` : Eutrophisation

### Labels (4)
- `has_bio_label` : Label bio
- `has_fair_trade` : Commerce équitable
- `has_recyclable_packaging` : Emballage recyclable
- `has_local_origin` : Origine locale

### Ingrédients problématiques (3)
- `has_palm_oil` : Huile de palme
- `has_high_sugar` : Teneur élevée en sucre
- `has_additives` : Additifs

### Compteurs (3)
- `ingredient_count` : Nombre d'ingrédients
- `allergen_count` : Nombre d'allergènes
- `label_count` : Nombre de labels

### Packaging (4)
- `packaging_type_plastique` : Plastique
- `packaging_type_verre` : Verre
- `packaging_type_papier` : Papier/Carton
- `packaging_type_metal` : Métal/Aluminium

---

## 🔧 Configuration

Variables d'environnement (`.env`) :

```env
# API
API_VERSION=1.0.0
PORT=8005

# Database
DATABASE_URL=postgresql://ecolabel:ecolabel123@localhost:5437/scoring

# ML Models
CLASSIFICATION_MODEL_PATH=app/models/classification_model.pkl
REGRESSION_MODEL_PATH=app/models/regression_model.pkl
```

---

## 📝 Endpoints

### POST `/score/calculate`

Calcule le score écologique.

**Body** :
```json
{
  "lca_data": {
    "co2_kg": 2.5,
    "water_liters": 500.0,
    "energy_mj": 8.0
  },
  "nlp_data": {
    "ingredients": [...],
    "has_bio_label": true,
    ...
  },
  "method": "hybrid"  // "classification", "regression", ou "hybrid"
}
```

### GET `/score/models/info`

Informations sur les modèles chargés.

### GET `/health`

Health check du service.

---

## 🧪 Entraînement des Modèles

Les modèles doivent être entraînés avec des données labellisées. Pour l'instant, le service utilise des modèles par défaut (non entraînés).

Pour entraîner les modèles :

1. Préparer un dataset avec features et scores réels
2. Utiliser scikit-learn pour entraîner
3. Sauvegarder avec `joblib`
4. Placer dans `app/models/`

---

## 🐛 Troubleshooting

### Erreur : "Modèle non entraîné"

Les modèles par défaut sont créés mais non entraînés. Pour utiliser des modèles entraînés :

1. Entraîner les modèles avec vos données
2. Sauvegarder dans `app/models/`
3. Redémarrer le service

### Erreur : "Database connection failed"

```bash
# Vérifier que PostgreSQL est démarré
docker-compose ps scoring-db

# Restart si nécessaire
docker-compose restart scoring-db
```

---

## 📄 Licence

MIT

---

## 🤝 Contribution

Les contributions sont les bienvenues !

