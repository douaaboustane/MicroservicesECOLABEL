# 🚀 API Gateway Service

Point d'entrée unique pour le frontend - Orchestration des microservices EcoLabel-MS.

## 🎯 Fonctionnalités

- ✅ **Point d'entrée unique** : Port 8000 pour le frontend Flutter
- ✅ **Orchestration** : Coordonne le workflow complet (OCR → NLP → LCA → Scoring)
- ✅ **Gestion de jobs** : Création, suivi et stockage des jobs asynchrones
- ✅ **Authentification JWT** : Protection des routes avec tokens JWT (implémenté et actif)
- ✅ **API REST** : Endpoints `/mobile/*` pour le frontend

---

## 📊 Workflow d'Orchestration

```
1. Frontend envoie image
   POST /mobile/products/scan
   ↓
2. API Gateway crée job (status: PENDING)
   ↓
3. API Gateway appelle Parser Service
   POST http://parser-service:8001/product/parse/single
   Status: OCR
   ↓
4. API Gateway appelle NLP Service
   POST http://nlp-service:8003/nlp/extract
   Status: NLP
   ↓
5. API Gateway appelle LCA Service
   POST http://lca-service:8004/lca/calc
   Status: ACV
   ↓
6. API Gateway appelle Scoring Service
   POST http://scoring-service:8005/score/calculate
   Status: SCORE
   ↓
7. API Gateway sauvegarde le résultat
   Status: DONE
   ↓
8. Frontend récupère le résultat
   GET /mobile/products/scan/{id}/status
```

---

## 🚀 Installation & Démarrage

### Option 1 : Docker (Recommandé)

```bash
# Depuis la racine du projet
docker-compose up --build api-gateway

# L'API sera disponible sur http://localhost:8000
# Documentation Swagger: http://localhost:8000/docs
```

### Option 2 : Local

```bash
cd backend/api-gateway-service

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env
cp .env.example .env

# Lancer le service
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📖 API Documentation

### Swagger UI

Une fois le service démarré, accédez à la documentation interactive :

👉 **http://localhost:8000/docs**

---

## 🔌 Endpoints Principaux

### POST `/mobile/products/scan`

Crée un nouveau job de scan de produit.

**Request** :
- `file` : Image du produit (multipart/form-data)

**Response** :
```json
{
  "job_id": "uuid-1234",
  "status": "PENDING",
  "created_at": "2025-12-28T14:00:00Z"
}
```

---

### GET `/mobile/products/scan/{job_id}/status`

Récupère le statut d'un job (utilisé pour le polling).

**Response** (en cours) :
```json
{
  "job_id": "uuid-1234",
  "status": "NLP",
  "progress": 40,
  "current_step": "Extraction des ingrédients (NLP)",
  "created_at": "2025-12-28T14:00:00Z",
  "updated_at": "2025-12-28T14:00:05Z"
}
```

**Response** (terminé) :
```json
{
  "job_id": "uuid-1234",
  "status": "DONE",
  "progress": 100,
  "result": {
    "score_letter": "B",
    "score_value": 72.5,
    "confidence": 0.85,
    "acv_data": {
      "co2_kg": 2.5,
      "water_liters": 500.0,
      "energy_mj": 8.0
    },
    "ingredients": ["farine de blé", "eau", "sel"],
    "allergens": ["gluten"]
  }
}
```

---

### POST `/mobile/auth/login`

Connexion utilisateur.

**Request** :
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response** :
```json
{
  "user": {
    "id": "user-123",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### POST `/mobile/auth/signup`

Inscription utilisateur.

**Request** :
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}
```

---

## 🔧 Configuration

Variables d'environnement (`.env`) :

```env
# API
API_VERSION=1.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://ecolabel:ecolabel123@api-db:5432/ecolabel_api

# Microservices URLs
PARSER_SERVICE_URL=http://parser-service:8001
NLP_SERVICE_URL=http://nlp-service:8003
LCA_SERVICE_URL=http://lca-service:8004
SCORING_SERVICE_URL=http://scoring-service:8005

# Auth
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

---

## 📁 Structure

```
api-gateway-service/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app
│   ├── config.py                  # Configuration
│   ├── database.py                # PostgreSQL
│   ├── models.py                  # SQLAlchemy models (Job, User)
│   ├── schemas.py                 # Pydantic schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── orchestrator.py        # Orchestration workflow
│   │   ├── job_manager.py         # Gestion jobs
│   │   ├── auth_service.py        # Authentification JWT
│   │   └── client_service.py     # Client HTTP pour microservices
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── mobile.py              # Routes /mobile/*
│   │   └── auth.py                 # Routes /mobile/auth/*
│   └── utils/
│       └── __init__.py
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🧪 Tests

```bash
# Tests unitaires (à implémenter)
pytest tests/ -v

# Test manuel avec curl
curl -X POST http://localhost:8000/mobile/products/scan \
  -F "file=@product.jpg"

# Vérifier le statut
curl http://localhost:8000/mobile/products/scan/{job_id}/status
```

---

## 🔄 Communication avec les Microservices

L'API Gateway communique avec les microservices via HTTP dans le réseau Docker :

- **Parser Service** : `http://parser-service:8001`
- **NLP Service** : `http://nlp-service:8003`
- **LCA Service** : `http://lca-service:8004`
- **Scoring Service** : `http://scoring-service:8005`

Tous les services sont sur le réseau `ecolabel-network` défini dans `docker-compose.yml`.

---

## 📝 Notes

- Le traitement est **asynchrone** : le frontend reçoit immédiatement un `job_id` et fait du polling
- Les jobs sont stockés en **PostgreSQL** (table `jobs`)
- L'authentification utilise **JWT** (JSON Web Tokens) - **Implémentée et active**
- Les routes peuvent être **protégées** (token requis) ou **optionnelles** (token optionnel)
- Les erreurs sont capturées et stockées dans `job.error_message`

## 🔐 Authentification

L'authentification JWT est **implémentée et active**. Voir le guide complet :

👉 **[AUTH_GUIDE.md](./AUTH_GUIDE.md)**

### Routes Protégées (Token Requis)

- `GET /mobile/auth/me` - Récupérer l'utilisateur actuel
- `PATCH /mobile/auth/me` - Mettre à jour le profil

### Routes Optionnelles (Token Optionnel)

- `POST /mobile/products/scan` - Créer un job (fonctionne avec ou sans token)
- `GET /mobile/products/scan/{id}/status` - Statut du job (fonctionne avec ou sans token)

### Routes Publiques (Pas de Token)

- `POST /mobile/auth/login` - Connexion
- `POST /mobile/auth/signup` - Inscription

---

## 🚧 Améliorations Futures

- [ ] Implémenter l'authentification JWT complète (middleware)
- [ ] Ajouter des tests unitaires et d'intégration
- [ ] Implémenter un système de retry automatique
- [ ] Ajouter des métriques et monitoring
- [ ] Migrer vers RabbitMQ si besoin de scalabilité

---

**Fait avec ❤️ par l'équipe EcoLabel-MS** 🌍

