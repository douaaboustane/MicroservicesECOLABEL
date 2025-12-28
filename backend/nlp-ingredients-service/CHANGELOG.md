# Changelog - NLP-Ingredients Service

## Version 1.2.0 - Fonctionnalités Essentielles (2025-12-27)

### ✨ Nouveautés

- **PackagingExtractor** : Nouveau service d'extraction des emballages
  - Détection de 7 types d'emballage (plastique, verre, papier, carton, métal, bois, bioplastique)
  - Détection recyclable/non recyclable
  - Extraction du poids de l'emballage (g, kg)
  - Facteurs d'impact environnemental (ADEME) pour chaque type
  - Patterns multilingues (FR + EN)

- **OriginExtractor** : Nouveau service d'extraction de la provenance
  - Détection de provenance (France, Europe, local, Espagne, Italie, etc.)
  - Détection de labels géographiques (AOC, AOP, IGP, STG)
  - Facteurs d'impact transport (ADEME)
  - Distances moyennes estimées par provenance
  - Patterns multilingues (FR + EN)

- **Scripts DB** : Script d'initialisation de la base de données
  - `scripts/init_database.py` : Peuple les tables PostgreSQL avec les taxonomies

### 🔧 Améliorations

- **API enrichie** : Nouveaux paramètres dans `ExtractRequest`
  - `detect_packaging` : Active/désactive la détection d'emballage (défaut: True)
  - `detect_origin` : Active/désactive la détection de provenance (défaut: True)

- **Réponse enrichie** : `ExtractResponse` inclut maintenant
  - `packaging` : Informations sur l'emballage détecté
  - `origin` : Informations sur la provenance détectée

- **Schemas étendus** :
  - Nouveau schéma `Packaging` avec tous les détails
  - Nouveau schéma `Origin` avec labels géographiques

### 📊 Conformité avec le Document

- ✅ Extraction emballage : 100% conforme
- ✅ Extraction provenance : 100% conforme
- ✅ Scripts DB : 100% conforme
- ✅ Structure conservée (simple et maintenable)

---

## Version 1.1.0 - Intégration Data Pipeline (2025-12-27)

### ✨ Nouveautés

- **TaxonomyLoader** : Nouveau service de chargement automatique des taxonomies
  - Support multi-sources (JSON + CSV)
  - Fusion intelligente de plusieurs taxonomies
  - Statistiques détaillées sur les données chargées

- **Intégration Agribalyse** : Base de données complète
  - 3,296 produits alimentaires avec codes Agribalyse
  - Impacts environnementaux (CO2, eau, énergie, etc.)
  - Matching automatique lors de la normalisation

- **Nouveau endpoint** : `GET /nlp/taxonomy/stats`
  - Statistiques complètes sur la taxonomie
  - Comptage par catégorie
  - Nombre d'ingrédients avec codes Agribalyse/EcoInvent

### 🔧 Améliorations

- **Startup amélioré** : Affichage détaillé des ressources au démarrage
  - Modèle NER : version, labels, performance
  - Taxonomie : nombre d'items, sources, statistiques

- **Normalisation améliorée** : Utilise maintenant la taxonomie complète
  - Matching avec codes Agribalyse
  - Fuzzy matching plus précis
  - Support des synonymes

---

## Version 1.0.0 - Version Initiale (2025-12-27)

### ✨ Fonctionnalités

- Extraction NER avec spaCy v3.0
- Normalisation des entités
- Détection de labels (bio, équitable, etc.)
- API REST avec FastAPI
- PostgreSQL pour stockage
- Docker & docker-compose
- Tests unitaires et API

### 🎯 Performances

- F1-Score global: 98.70%
- F1 INGREDIENT: 98.76%
- F1 ALLERGEN: 98.97%
- F1 QUANTITY: 78.57%

### 📖 API Endpoints

- `POST /nlp/extract` - Extraction et normalisation
- `POST /nlp/extract/batch` - Extraction en batch
- `GET /nlp/model/info` - Informations modèle
- `GET /health` - Health check
