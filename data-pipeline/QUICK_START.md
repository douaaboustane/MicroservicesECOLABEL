# Quick Start - Data Pipeline EcoLabel-MS

## Installation rapide

```bash
cd data-pipeline
python -m venv venv
source venv/bin/activate
make install
```

## Premiers pas

### 1. Tester le scraper Open Food Facts (5 min)

```bash
# Modifier config pour tester avec 100 produits
python 1_scrapers/openfoodfacts_scraper.py
```

### 2. Voir les données

```bash
python -c "import pandas as pd; df = pd.read_csv('datasets/raw/openfoodfacts_100k.csv.gz'); print(df.head())"
```

### 3. Lancer Jupyter

```bash
make notebooks
# Ouvrir: 3_exploration/notebooks/01_initial_eda.ipynb
```

## Commandes utiles

```bash
# Pipeline complet
make full

# Étapes individuelles
make scrape
make clean
make explore
make preprocess
make train

# Tests
make test
```

## Structure des données

```
datasets/
├── raw/           # Données brutes (scraping)
├── cleaned/       # Données nettoyées
├── processed/     # Prêt pour ML
├── reference/     # Taxonomies
└── models/        # Modèles entraînés
```

## Problèmes courants

**Tesseract non installé** : Le parser service en a besoin
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt-get install tesseract-ocr
```

**spaCy model manquant**
```bash
python -m spacy download fr_core_news_md
```

**Port PostgreSQL occupé**
Modifier `config/database_config.yaml` : port 5433

## Prochaines étapes

1. Collecter ~10K produits (30min) : `make scrape`
2. Nettoyer données (5min) : `make clean`
3. Explorer dans Jupyter : `make notebooks`
4. Entraîner modèle NER (optionnel, 2-3h) : `make train`

