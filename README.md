


[![Watch the video]("C:\Users\doaa\Downloads\videoDEMO.mp4")]
EcoLabel - Système d'Évaluation Écologique de Produits Alimentaires
Description du Projet
EcoLabel est une plateforme microservices permettant l'évaluation écologique automatisée de produits alimentaires à partir de photos. Le système analyse les images de produits, extrait les informations textuelles, identifie les ingrédients et calcule un score écologique basé sur l'analyse du cycle de vie (LCA).

Architecture
Le projet suit une architecture microservices avec les composants suivants:

Backend (Python/FastAPI)
API Gateway Service (Port 8000) - Point d'entrée unique, orchestration des workflows et authentification JWT
Parser Service (Port 8001) - Extraction de texte par OCR (Tesseract/EasyOCR)
NLP Ingredients Service (Port 8003) - Reconnaissance d'entités nommées (NER) pour identifier les ingrédients
LCA Lite Service (Port 8002) - Analyse du cycle de vie des ingrédients
Scoring Service (Port 8004) - Calcul du score écologique final
Frontend
Application Flutter - Interface mobile multiplateforme (iOS/Android/Web)
Infrastructure
PostgreSQL - Bases de données pour chaque service (Ports 5433-5436)
RabbitMQ - File d'attente de messages pour le traitement asynchrone (Port 5672)
Docker & Docker Compose - Conteneurisation et orchestration
Data Pipeline
Pipeline complet de données pour l'entraînement des modèles NLP:

Scrapers - Collecte de données (Open Food Facts, Agribalyse)
Cleaning - Nettoyage et validation des données
Exploration - Analyse statistique et visualisations
Preprocessing - Auto-annotation et augmentation de données
Training - Entraînement des modèles SpaCy NER
Prérequis
Docker et Docker Compose
Flutter SDK (pour le frontend)
Python 3.11+ (pour le développement local)
PostgreSQL 15
RabbitMQ
Installation et Démarrage
1. Cloner le Projet
git clone <repository-url>
cd MicroservicesECOLABEL
2. Démarrer les Services Backend
# Lancer tous les services avec Docker Compose
docker-compose up -d

# Vérifier le statut des services
docker-compose ps

# Voir les logs
docker-compose logs -f
Les services seront disponibles sur:

API Gateway: http://localhost:8000
Parser Service: http://localhost:8001
LCA Service: http://localhost:8002
NLP Service: http://localhost:8003
Scoring Service: http://localhost:8004
3. Démarrer le Frontend Flutter
cd frontend

# Installer les dépendances
flutter pub get

# Lancer sur iOS Simulator
flutter run -d <device-id>

# Lister les appareils disponibles
flutter devices
4. Configuration
Configurer l'URL de l'API Gateway dans le frontend:

// frontend/lib/core/config/env.dart
static const String apiBaseUrl = 'http://localhost:8000';
Utilisation
Workflow Complet
Upload d'Image - L'utilisateur prend ou sélectionne une photo de produit
Extraction OCR - Le Parser Service extrait le texte de l'image
Analyse NLP - Le NLP Service identifie les ingrédients
Évaluation LCA - Le LCA Service évalue l'impact environnemental
Calcul du Score - Le Scoring Service calcule le score écologique final
Résultat - L'utilisateur reçoit le score et les détails de l'analyse
API Endpoints Principaux
# Authentification
POST /auth/register
POST /auth/login

# Scan de produit
POST /mobile/products/scan

# Récupération du résultat
GET /mobile/jobs/{job_id}

# Historique
GET /mobile/jobs/history
Tests
Tester les Services Backend
# Test de santé global
python tests/test_services_health.py

# Test du workflow complet
python tests/test_workflow_complete.py

# Test OCR direct
python tests/test_ocr_direct.py
Tester le Frontend
cd frontend
flutter test
Data Pipeline
Pour entraîner ou réentraîner les modèles NLP:

cd data-pipeline

# Installer les dépendances
pip install -r requirements.txt

# Exécuter le pipeline complet
make all

# Ou étape par étape
make scrape    # Collecte des données
make clean     # Nettoyage
make explore   # Exploration
make preprocess # Prétraitement
make train     # Entraînement
Structure du Projet
MicroservicesECOLABEL/
├── backend/                      # Services backend
│   ├── api-gateway-service/      # Orchestrateur et authentification
│   ├── parser-service/           # OCR et extraction de texte
│   ├── nlp-ingredients-service/  # NER et analyse d'ingrédients
│   ├── lca-lite-service/         # Analyse du cycle de vie
│   └── scoring-service/          # Calcul de scores
├── frontend/                     # Application Flutter
│   ├── lib/                      # Code source Dart
│   └── assets/                   # Ressources (images, etc.)
├── data-pipeline/                # Pipeline de données ML
│   ├── 1_scrapers/               # Collecte de données
│   ├── 2_cleaning/               # Nettoyage
│   ├── 3_exploration/            # Analyse exploratoire
│   ├── 4_preprocessing/          # Prétraitement
│   └── 5_training/               # Entraînement des modèles
├── evaluation/                   # Scripts d'évaluation
├── tests/                        # Tests d'intégration
└── docker-compose.yml            # Configuration Docker
Technologies Utilisées
Backend
Python 3.11
FastAPI
SQLAlchemy
PostgreSQL
RabbitMQ
Tesseract OCR / EasyOCR
SpaCy (NER)
JWT Authentication
Frontend
Flutter / Dart
HTTP Client
Provider (State Management)
Image Picker
DevOps
Docker
Docker Compose
Git
Maintenance et Développement
Arrêter les Services
docker-compose down

# Avec suppression des volumes
docker-compose down -v
Reconstruire les Services
docker-compose build
docker-compose up -d
Logs et Debugging
# Logs d'un service spécifique
docker-compose logs -f api-gateway-service

# Accéder à un conteneur
docker exec -it api-gateway-service bash

# Vérifier la base de données
docker exec -it parser-postgres psql -U ecolabel -d ecolabel
