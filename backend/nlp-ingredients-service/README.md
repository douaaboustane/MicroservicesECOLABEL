# 🧠 NLP-Ingredients Service

Service d'extraction et normalisation des ingrédients utilisant NLP (spaCy NER v3.0).

## 🎯 Fonctionnalités

- ✅ **Extraction NER** : Détecte ingrédients, allergènes, quantités
- ✅ **E-numbers** : Détection E100-E1999
- ✅ **Minéraux** : CALCIUM, MAGNESIUM, SODIUM, etc.
- ✅ **Vitamines** : A, B1-B12, C, D, E, K
- ✅ **Normalisation** : Matching avec taxonomies (Agribalyse, EcoInvent)
- ✅ **Labels** : Détection bio, équitable, recyclable, local, etc.
- ✅ **Emballage** : Détection type d'emballage (plastique, verre, papier, etc.)
- ✅ **Provenance** : Détection origine géographique (France, Europe, local, etc.)
- ✅ **API REST** : FastAPI avec Swagger UI

---

## 📊 Performances du Modèle NER v3.0

| Métrique | Score |
|----------|-------|
| **F1-Score global** | **98.70%** |
| F1 INGREDIENT | 98.76% |
| F1 ALLERGEN | 98.97% |
| F1 QUANTITY | 78.57% |

---

## 🚀 Installation & Démarrage

### Option 1 : Docker (Recommandé)

```bash
# Construire et démarrer
cd backend/nlp-ingredients-service
docker-compose up --build

# L'API sera disponible sur http://localhost:8003

# Au démarrage, vous verrez :
# ✅ Modèle NER chargé: ner_ingredients_v3 (F1: 98.70%)
# ✅ Taxonomie chargée: 3,296+ ingrédients (Agribalyse + taxonomie locale)
```

### Option 2 : Local

```bash
# Installer les dépendances
pip install -r requirements.txt

# Télécharger le modèle spaCy français
python -m spacy download fr_core_news_md

# Créer le fichier .env
cp .env.example .env

# Lancer le service
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

---

## 📖 API Documentation

### Swagger UI

Une fois le service démarré, accédez à la documentation interactive :

👉 **http://localhost:8003/docs**

### Endpoints supplémentaires

- `GET /nlp/taxonomy/stats` - Statistiques sur la taxonomie chargée
- `GET /nlp/model/info` - Informations sur le modèle NER

### Nouvelles fonctionnalités (v1.1.0)

- `detect_packaging` : Détection automatique du type d'emballage
- `detect_origin` : Détection automatique de la provenance

---

## 🔥 Exemples d'Utilisation

### 1️⃣ Extraction Basique

```bash
curl -X POST "http://localhost:8003/nlp/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "farine de blé, eau, sel, levure"
  }'
```

**Résultat :**
```json
{
  "entities": [
    {"text": "farine", "label": "INGREDIENT", "start": 0, "end": 6},
    {"text": "blé", "label": "ALLERGEN", "start": 10, "end": 13},
    {"text": "eau", "label": "INGREDIENT", "start": 15, "end": 18}
  ],
  "entities_normalized": [
    {
      "text": "farine",
      "normalized_name": "farine",
      "category": "cereales",
      "agribalyse_code": "10019",
      "match_score": 100.0,
      "match_method": "exact"
    }
  ],
  "total_ingredients": 3,
  "total_allergens": 1
}
```

### 2️⃣ E-Numbers

```bash
curl -X POST "http://localhost:8003/nlp/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "colorant E150d, conservateur E330, émulsifiant E471"
  }'
```

### 3️⃣ Minéraux (Eau Minérale)

```bash
curl -X POST "http://localhost:8003/nlp/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "CALCIUM 55 MAGNESIUM 19 SODIUM 24 POTASSIUM 12"
  }'
```

### 4️⃣ Avec Détection de Labels

```bash
curl -X POST "http://localhost:8003/nlp/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Farine bio de blé tendre, sucre équitable, emballage recyclable",
    "detect_labels": true
  }'
```

### 5️⃣ Avec Détection d'Emballage et Provenance

```bash
curl -X POST "http://localhost:8003/nlp/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Produit en France, emballage plastique recyclable 50g, fabriqué en France",
    "detect_packaging": true,
    "detect_origin": true
  }'
```

**Résultat :**
```json
{
  "packaging": {
    "type": "plastique",
    "text": "emballage plastique",
    "recyclable": true,
    "weight": 50.0,
    "weight_unit": "g",
    "confidence": 0.9
  },
  "origin": {
    "origin": "france",
    "text": "france",
    "confidence": 0.95,
    "geographic_labels": []
  }
}
```

**Résultat :**
```json
{
  "labels": [
    {"label_type": "bio", "label_name": "bio", "confidence": 0.9},
    {"label_type": "fair_trade", "label_name": "équitable", "confidence": 0.9},
    {"label_type": "recyclable", "label_name": "recyclable", "confidence": 0.85}
  ]
}
```

### 5️⃣ Extraction en Batch

```bash
curl -X POST "http://localhost:8003/nlp/extract/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "farine de blé, eau, sel",
      "lait, sucre, vanille",
      "CALCIUM 55 SODIUM 24"
    ]
  }'
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│ FastAPI (Port 8003)                 │
│  • POST /nlp/extract                │
│  • POST /nlp/extract/batch          │
│  • GET /nlp/model/info              │
│  • GET /health                      │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ NER Extractor (spaCy v3.0)          │
│  • F1-Score: 98.70%                 │
│  • Labels: INGREDIENT, ALLERGEN,    │
│    QUANTITY                         │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ Entity Normalizer                   │
│  • Matching Agribalyse              │
│  • Matching EcoInvent               │
│  • Fuzzy Search                     │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ Label Detector                      │
│  • Bio, Équitable, Recyclable       │
│  • Local, AOC, IGP, etc.            │
└─────────────────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│ PostgreSQL                          │
│  • Taxonomies                       │
│  • Historique extractions           │
└─────────────────────────────────────┘
```

---

## 🧪 Tests

```bash
# Installer pytest
pip install pytest pytest-asyncio httpx

# Lancer les tests
pytest tests/ -v

# Avec coverage
pytest tests/ --cov=app --cov-report=html
```

---

## 📊 Données & Taxonomies

### Fichiers de Taxonomie

- `app/data/taxonomies/ingredients.json` : Taxonomie des ingrédients
- `app/data/taxonomies/agribalyse.json` : Mapping Agribalyse (à créer)
- `app/data/taxonomies/ecoinvent.json` : Mapping EcoInvent (à créer)

### Format de la Taxonomie

```json
{
  "farine": {
    "category": "cereales",
    "agribalyse_code": "10019",
    "ecoinvent_code": "wheat_flour_FR",
    "synonyms": ["farine de ble", "wheat flour"],
    "is_allergen": false
  },
  "lait": {
    "category": "produits_laitiers",
    "agribalyse_code": "19001",
    "allergen_category": "lait",
    "synonyms": ["milk", "lait entier"],
    "is_allergen": true
  }
}
```

---

## 🔧 Configuration

Variables d'environnement (`.env`) :

```env
# API
API_VERSION=1.0.0
PORT=8003

# Database
DATABASE_URL=postgresql://ecolabel:ecolabel123@localhost:5434/nlp_ingredients

# NLP Models
NER_MODEL_PATH=app/models/ner_ingredients_v3
FUZZY_THRESHOLD=80
```

---

## 🐛 Troubleshooting

### Erreur : "Modèle NER non chargé"

```bash
# Vérifier que le modèle existe
ls app/models/ner_ingredients_v3/

# Si absent, copier depuis data-pipeline
cp -r ../../data-pipeline/models/ner_ingredients_v3 app/models/
```

### Erreur : "Database connection failed"

```bash
# Vérifier que PostgreSQL est démarré
docker-compose ps

# Restart si nécessaire
docker-compose restart postgres
```

---

## 📝 TODO

- [ ] Ajouter plus d'ingrédients à la taxonomie
- [ ] Intégrer Agribalyse complet
- [ ] Ajouter BERT multilingue pour classification
- [ ] Améliorer le matching fuzzy
- [ ] Ajouter cache Redis pour les résultats

---

## 👨‍💻 Développement

### Structure du Projet

```
nlp-ingredients-service/
├── app/
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── database.py          # PostgreSQL
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── services/
│   │   ├── ner_extractor.py      # NER extraction
│   │   ├── normalizer.py         # Normalisation
│   │   └── label_detector.py     # Détection labels
│   ├── models/
│   │   └── ner_ingredients_v3/   # Modèle NER
│   └── data/
│       └── taxonomies/           # Taxonomies JSON
├── tests/                   # Tests pytest
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 📄 Licence

MIT

---

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing`)
5. Créer une Pull Request

---

## 📞 Support

Pour toute question ou bug, ouvrez une issue sur GitHub.

---

**Fait avec ❤️ par l'équipe EcoLabel-MS** 🌍

