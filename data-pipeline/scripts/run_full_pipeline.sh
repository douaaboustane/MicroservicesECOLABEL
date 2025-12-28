#!/bin/bash

# ============================================
# Pipeline Complet EcoLabel Data Mining
# ============================================

set -e  # Exit on error

echo "╔════════════════════════════════════════════╗"
echo "║  ECOLABEL DATA MINING PIPELINE v1.0        ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Timestamps
START_TIME=$(date +%s)

# ============================================
# ÉTAPE 1 : SCRAPING
# ============================================
echo -e "${BLUE}[1/5] COLLECTE DE DONNÉES${NC}"
echo "  → Open Food Facts..."
python 1_scrapers/openfoodfacts_scraper.py

echo "  → Agribalyse..."
python 1_scrapers/agribalyse_downloader.py

echo -e "${GREEN}✓ Scraping terminé${NC}\n"

# ============================================
# ÉTAPE 2 : CLEANING
# ============================================
echo -e "${BLUE}[2/5] NETTOYAGE DES DONNÉES${NC}"
python 2_cleaning/normalizer.py
echo -e "${GREEN}✓ Nettoyage terminé${NC}\n"

# ============================================
# RÉSUMÉ
# ============================================
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "╔════════════════════════════════════════════╗"
echo "║           PIPELINE TERMINÉ ✓               ║"
echo "╚════════════════════════════════════════════╝"
echo "Durée: $((DURATION / 60)) min $((DURATION % 60)) sec"

