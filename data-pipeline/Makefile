.PHONY: help install scrape clean explore preprocess train full notebooks test

help:
	@echo "╔════════════════════════════════════════════╗"
	@echo "║  EcoLabel Data Pipeline - Commandes       ║"
	@echo "╚════════════════════════════════════════════╝"
	@echo ""
	@echo "make install     - Installer dépendances"
	@echo "make scrape      - Scraping uniquement"
	@echo "make clean       - Nettoyage données"
	@echo "make explore     - Analyse exploratoire"
	@echo "make preprocess  - Preprocessing ML"
	@echo "make train       - Entraînement modèle"
	@echo "make full        - Pipeline complet"
	@echo "make notebooks   - Lancer Jupyter Lab"
	@echo "make test        - Lancer tests unitaires"

install:
	@echo "📦 Installation des dépendances..."
	pip install -r requirements.txt
	python -m spacy download fr_core_news_md
	@echo "✅ Installation terminée"

scrape:
	@echo "🕷️  Scraping en cours..."
	python 1_scrapers/openfoodfacts_scraper.py
	python 1_scrapers/agribalyse_downloader.py
	@echo "✅ Scraping terminé"

clean:
	@echo "🧹 Nettoyage des données..."
	python 2_cleaning/deduplicator.py
	python 2_cleaning/normalizer.py
	python 2_cleaning/schema_validator.py
	python 2_cleaning/missing_handler.py
	@echo "✅ Nettoyage terminé"

explore:
	@echo "📊 Analyse exploratoire..."
	python 3_exploration/statistics.py
	python 3_exploration/visualizations.py
	python 3_exploration/correlations.py
	@echo "✅ Exploration terminée"

preprocess:
	@echo "⚙️  Preprocessing ML..."
	python 4_preprocessing/tokenizer.py
	python 4_preprocessing/auto_annotator.py
	python 4_preprocessing/data_augmentation.py
	python 4_preprocessing/train_test_splitter.py
	@echo "✅ Preprocessing terminé"

train:
	@echo "🧠 Entraînement du modèle..."
	python 5_training/train_spacy_ner.py
	python 5_training/evaluate_model.py
	@echo "✅ Entraînement terminé"

full:
	@echo "🚀 Exécution pipeline complet..."
	bash scripts/run_full_pipeline.sh

notebooks:
	@echo "📓 Lancement Jupyter Lab..."
	jupyter lab 3_exploration/notebooks/

test:
	@echo "🧪 Lancement des tests..."
	pytest tests/ -v

