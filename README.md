


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

Les services seront disponibles sur:

API Gateway: http://localhost:8000
Parser Service: http://localhost:8001
LCA Service: http://localhost:8002
NLP Service: http://localhost:8003
Scoring Service: http://localhost:8004

 la base de données
docker exec -it parser-postgres psql -U ecolabel -d ecolabel
