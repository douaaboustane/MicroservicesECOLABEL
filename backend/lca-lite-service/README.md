# 🌍 LCA-Lite Service

Service de calcul d'Analyse du Cycle de Vie simplifiée pour les produits alimentaires.

## 🎯 Fonctionnalités

- ✅ **Calcul ACV complet** : CO2, eau, énergie, acidification, eutrophisation
- ✅ **Base Agribalyse** : 3,296 produits avec impacts détaillés
- ✅ **Impact ingrédients** : Calcul pondéré par quantité
- ✅ **Impact emballage** : 7 types d'emballage (plastique, verre, papier, etc.)
- ✅ **Impact transport** : Routier, aérien, maritime, ferroviaire
- ✅ **Agrégation** : Décomposition par catégorie (ingrédients/emballage/transport)
- ✅ **API REST** : FastAPI avec Swagger UI

---

## 🚀 Installation & Démarrage

### Option 1 : Docker (Recommandé)

```bash
cd backend/lca-lite-service
docker-compose up --build

# L'API sera disponible sur http://localhost:8004
```

### Option 2 : Local

```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8004 --reload
```

---

## 📖 API Documentation

### Swagger UI

👉 **http://localhost:8004/docs**

---

## 🔥 Exemple d'Utilisation

### Calcul ACV pour un pain

```bash
curl -X POST "http://localhost:8004/lca/calc" \
  -H "Content-Type: application/json" \
  -d '{
    "ingredients": [
      {
        "name": "farine de blé",
        "agribalyse_code": "10019",
        "quantity_percentage": 60
      },
      {
        "name": "eau",
        "quantity_percentage": 30
      },
      {
        "name": "levure",
        "quantity_percentage": 5
      },
      {
        "name": "sel",
        "quantity_percentage": 2
      },
      {
        "name": "sucre",
        "quantity_percentage": 3
      }
    ],
    "packaging": {
      "type": "plastique",
      "weight_g": 50,
      "recyclable": true
    },
    "transport": {
      "origin_country": "FR",
      "destination_country": "FR",
      "transport_type": "routier_france",
      "distance_km": 200
    },
    "product_weight_kg": 0.5
  }'
```

### Résultat

```json
{
  "total_impacts": {
    "co2_kg": 0.813,
    "water_m3": 0.015,
    "energy_mj": 7.2,
    "acidification": 0.0042,
    "eutrophisation": 0.0031
  },
  "breakdown": {
    "ingredients": {
      "co2_kg": 0.613,
      "water_m3": 0.014,
      "energy_mj": 6.5,
      "contribution_percentage": 75.4
    },
    "packaging": {
      "co2_kg": 0.15,
      "water_m3": 0.001,
      "energy_mj": 2.25,
      "contribution_percentage": 18.5
    },
    "transport": {
      "co2_kg": 0.05,
      "contribution_percentage": 6.1
    }
  },
  "ingredients_impacts": [
    {
      "ingredient_name": "farine de blé",
      "quantity_kg": 0.3,
      "impacts": {
        "co2_kg": 0.498,
        "water_m3": 0.0036
      },
      "agribalyse_code": "10019"
    }
  ],
  "product_weight_kg": 0.5,
  "processing_time_ms": 45.2
}
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│ FastAPI (Port 8004)                 │
│  • POST /lca/calc                   │
│  • GET /health                      │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ LCAService                          │
│  • Orchestration calculs            │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ Calculators                         │
│  • IngredientImpactCalculator       │
│  • PackagingImpactCalculator        │
│  • TransportImpactCalculator        │
│  • ImpactAggregator                 │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ Databases                           │
│  • AgribalyseDB (3,296 produits)    │
│  • Transport Factors (JSON)         │
│  • Packaging Impacts (JSON)         │
└─────────────────────────────────────┘
```

---

## 📊 Indicateurs Calculés

| Indicateur | Unité | Description |
|------------|-------|-------------|
| **CO2** | kg CO2 eq | Changement climatique |
| **Eau** | m³ | Consommation d'eau |
| **Énergie** | MJ | Consommation d'énergie |
| **Acidification** | mol H+ eq | Potentiel d'acidification |
| **Eutrophisation** | mol N eq | Potentiel d'eutrophisation |

---

## 🔧 Configuration

Variables d'environnement (`.env`) :

```env
DATABASE_URL=postgresql://ecolabel:ecolabel123@localhost:5435/lca_lite
AGRIBALYSE_FILE=app/data/agribalyse_processed.csv
PORT=8004
```

---

## 📁 Structure

```
lca-lite-service/
├── app/
│   ├── main.py                    # FastAPI app
│   ├── config.py                  # Configuration
│   ├── database.py                # PostgreSQL
│   ├── models.py                  # SQLAlchemy models
│   ├── schemas.py                 # Pydantic schemas
│   ├── calculators/               # Moteurs de calcul
│   ├── databases/                 # Interfaces bases de données
│   ├── services/                  # Business logic
│   └── data/                      # Données de référence
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 🧪 Tests

```bash
pytest tests/ -v
```

---

## 📞 Support

Pour toute question, ouvrez une issue sur GitHub.

---

**Fait avec ❤️ par l'équipe EcoLabel-MS** 🌍

