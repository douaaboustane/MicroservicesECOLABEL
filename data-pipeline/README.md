# Data Pipeline EcoLabel-MS

Pipeline de collecte, nettoyage et préparation des données pour l'entraînement des modèles ML.

## 🎯 Objectif

Créer des datasets de qualité pour alimenter les microservices EcoLabel-MS :
- **NLP Service** : Modèle NER pour extraction d'ingrédients
- **LCA Service** : Base de données d'impacts environnementaux
- **Scoring Service** : Algorithmes de calcul d'éco-score

## 📊 Architecture

```
data-pipeline/
├── 1_scrapers/          # Collecte de données (OFF, Agribalyse)
├── 2_cleaning/          # Nettoyage et validation
├── 3_exploration/       # Analyse exploratoire (EDA)
├── 4_preprocessing/     # Preprocessing ML
├── 5_training/          # Entraînement modèles spaCy
├── datasets/            # Données brutes, nettoyées, traitées
├── outputs/             # Rapports, visualisations, logs
├── config/              # Configuration YAML/JSON
├── utils/               # Utilitaires (logger, db, files)
└── scripts/             # Scripts d'orchestration
```

## 🚀 Installation

```bash
# 1. Créer environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Installer dépendances
make install
# OU
pip install -r requirements.txt
python -m spacy download fr_core_news_md

# 3. Copier configuration
cp .env.example .env
```

## 📝 Utilisation

### Pipeline complet (6-12h)

```bash
make full
# OU
bash scripts/run_full_pipeline.sh
```

### Étapes individuelles

```bash
make scrape      # Scraping uniquement (2-3h)
make clean       # Nettoyage données (30min)
make explore     # Analyse exploratoire (1h)
make preprocess  # Preprocessing ML (2h)
make train       # Entraînement modèle (3-4h)
```

### Jupyter Notebooks

```bash
make notebooks
# Ouvre Jupyter Lab dans 3_exploration/notebooks/
```

## 📦 Données générées

### Datasets

```
datasets/
├── raw/                           # Données brutes
│   ├── openfoodfacts_100k.csv.gz    → 100K produits OFF
│   └── agribalyse_2.5k.csv.gz       → Base impacts Agribalyse
│
├── cleaned/                       # Après nettoyage
│   └── products_cleaned.csv.gz      → Données validées
│
├── processed/                     # Prêt pour ML
│   ├── training_data.jsonl          → Entraînement
│   ├── validation_data.jsonl        → Validation
│   └── test_data.jsonl              → Test
│
├── reference/                     # Taxonomies
│   ├── ingredient_taxonomy.csv      → Liste ingrédients normalisés
│   └── ecoinvent_impacts.csv        → Impacts environnementaux
│
└── models/                        # Modèles entraînés
    └── spacy/
        └── ingredient_ner_v1/       → Modèle NER spaCy
```

### Rapports

```
outputs/
├── reports/
│   ├── eda_report.html              → Analyse exploratoire
│   └── model_evaluation.pdf         → Évaluation modèle
├── visualizations/
│   ├── ingredient_distribution.png
│   └── correlation_matrix.png
└── logs/
    └── pipeline.log                 → Logs d'exécution
```

## 🔌 Intégration avec Microservices

Les datasets générés sont copiés automatiquement vers les microservices :

```bash
# NLP Service
datasets/reference/ingredient_taxonomy.csv → backend/nlp-service/data/
datasets/models/spacy/ingredient_ner_v1/  → backend/nlp-service/models/

# LCA Service
datasets/reference/ecoinvent_impacts.csv  → backend/lca-service/data/
```

## ⚙️ Configuration

### pipeline_config.yaml

```yaml
scraping:
  openfoodfacts:
    max_products: 100000
    country: "France"
    rate_limit: 1

training:
  spacy:
    n_iter: 50
    batch_size: 32
    learning_rate: 0.001
```

### .env

```bash
DATABASE_URL=postgresql://ecolabel:ecolabel123@localhost:5433/ecolabel
LOG_LEVEL=INFO
SPACY_MODEL=fr_core_news_md
```

## 📊 Sources de Données

1. **Open Food Facts** (https://world.openfoodfacts.org)
   - 100K+ produits alimentaires
   - Ingrédients, labels, nutriscore
   - API publique gratuite

2. **Agribalyse** (https://agribalyse.ademe.fr)
   - Base impacts environnementaux ADEME
   - CO₂, eau, énergie par ingrédient
   - Données officielles françaises

## 🧪 Tests

```bash
make test
# OU
pytest tests/ -v
```

## 📄 Licence

Propriétaire - EcoLabel-MS

---

**Note** : Le scraping de sites e-commerce (Carrefour, Auchan) est désactivé par défaut. Vérifiez les CGU avant activation.

