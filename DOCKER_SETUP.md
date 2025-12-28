# 🐳 Docker Compose - Setup Guide

Guide pour lancer tous les microservices avec Docker Compose.

## 📋 Prérequis

- Docker Desktop installé (Windows/Mac) ou Docker + Docker Compose (Linux)
- Au moins 4GB de RAM disponible
- Ports libres : 8001, 8003, 8004, 5433, 5434, 5435, 5436

## 🚀 Démarrage rapide

### 1. Lancer tous les services (Recommandé)

```bash
# Depuis la racine du projet (Eco-projet/)
docker-compose up -d
```

Cette commande utilise le `docker-compose.yml` à la racine qui orchestre **tous les services** ensemble.

### 1bis. Développement local d'un seul service

Si vous voulez tester un seul service isolément (pour le développement) :

```bash
# Parser Service uniquement
cd backend/parser-service
docker-compose -f docker-compose.dev.yml up -d

# NLP Service uniquement
cd backend/nlp-ingredients-service
docker-compose -f docker-compose.dev.yml up -d

# LCA Service uniquement
cd backend/lca-lite-service
docker-compose -f docker-compose.dev.yml up -d
```

**Note** : Les fichiers `docker-compose.dev.yml` dans chaque microservice sont pour le développement local. Pour la production ou l'intégration complète, utilisez le `docker-compose.yml` à la racine.

Cette commande va :
- ✅ Créer 4 bases de données PostgreSQL
- ✅ Lancer les 3 microservices (Parser, NLP, LCA)
- ✅ Configurer le réseau Docker
- ✅ Créer les volumes persistants

### 2. Vérifier que tout fonctionne

```bash
# Voir les logs
docker-compose logs -f

# Voir les services en cours
docker-compose ps

# Tester les endpoints
curl http://localhost:8001/health  # Parser Service
curl http://localhost:8003/health  # NLP Service
curl http://localhost:8004/health   # LCA Service
```

### 3. Arrêter les services

```bash
# Arrêter sans supprimer les volumes
docker-compose stop

# Arrêter et supprimer les conteneurs (garder les volumes)
docker-compose down

# Arrêter et supprimer TOUT (volumes inclus)
docker-compose down -v
```

## 📊 Services disponibles

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| **Parser Service** | 8001 | http://localhost:8001 | OCR et parsing de fichiers |
| **NLP Service** | 8003 | http://localhost:8003 | Extraction d'entités NER |
| **LCA Service** | 8004 | http://localhost:8004 | Calcul d'impacts environnementaux |
| **API Gateway** | 8000 | http://localhost:8000 | ⚠️ À créer |

### Bases de données

| DB | Port | Container | Database |
|----|------|-----------|----------|
| Parser DB | 5433 | parser-postgres | ecolabel |
| NLP DB | 5434 | nlp-postgres | nlp_ingredients |
| LCA DB | 5435 | lca-postgres | lca_lite |
| API DB | 5436 | api-postgres | ecolabel_api |

## 🔧 Commandes utiles

### Rebuild un service spécifique

```bash
# Rebuild et redémarrer un service
docker-compose up -d --build parser-service

# Rebuild tous les services
docker-compose build
docker-compose up -d
```

### Voir les logs d'un service

```bash
# Logs en temps réel
docker-compose logs -f parser-service

# Dernières 100 lignes
docker-compose logs --tail=100 nlp-service
```

### Accéder à une base de données

```bash
# Se connecter à la DB Parser
docker exec -it parser-postgres psql -U ecolabel -d ecolabel

# Se connecter à la DB NLP
docker exec -it nlp-postgres psql -U ecolabel -d nlp_ingredients
```

### Nettoyer

```bash
# Supprimer les conteneurs arrêtés
docker-compose rm

# Supprimer les images non utilisées
docker image prune

# Nettoyage complet (⚠️ supprime tout)
docker system prune -a --volumes
```

## 🔍 Dépannage

### Port déjà utilisé

```bash
# Voir quel processus utilise le port
netstat -ano | findstr :8001  # Windows
lsof -i :8001                  # Mac/Linux

# Changer le port dans docker-compose.yml
ports:
  - "8002:8001"  # Au lieu de 8001:8001
```

### Service ne démarre pas

```bash
# Voir les logs d'erreur
docker-compose logs parser-service

# Vérifier les healthchecks
docker-compose ps

# Redémarrer un service
docker-compose restart parser-service
```

### Base de données non accessible

```bash
# Vérifier que la DB est prête
docker exec parser-postgres pg_isready -U ecolabel

# Voir les logs de la DB
docker-compose logs parser-db
```

### Modèle NER non trouvé

Le modèle NER doit être présent dans `backend/nlp-ingredients-service/app/models/ner_ingredients_v3/`

Si absent, copier depuis `data-pipeline/models/ner_ingredients_v3/`

## 🌐 Communication entre services

Les services communiquent via le réseau Docker `ecolabel-network` :

- **Nom de service** : Utiliser le nom du service (ex: `parser-service`)
- **Port interne** : Utiliser le port du conteneur (ex: `8001`)
- **URL complète** : `http://parser-service:8001`

### Exemple depuis l'API Gateway (futur)

```python
# Dans l'API Gateway
PARSER_SERVICE_URL = "http://parser-service:8001"
NLP_SERVICE_URL = "http://nlp-service:8003"
LCA_SERVICE_URL = "http://lca-service:8004"
```

## 📝 Variables d'environnement

Les variables sont définies dans `docker-compose.yml`. Pour les modifier :

1. Créer un fichier `.env` à la racine
2. Définir les variables
3. Référencer dans `docker-compose.yml` avec `${VARIABLE}`

Exemple `.env` :
```env
POSTGRES_PASSWORD=your_secure_password
JWT_SECRET=your_jwt_secret
```

## 🎯 Prochaines étapes

1. ✅ Docker Compose créé
2. ⏳ Créer l'API Gateway Service
3. ⏳ Ajouter l'API Gateway au docker-compose.yml
4. ⏳ Configurer les variables d'environnement
5. ⏳ Tests d'intégration

## 📚 Documentation

- [Parser Service README](../backend/parser-service/README.md)
- [NLP Service README](../backend/nlp-ingredients-service/README.md)
- [LCA Service README](../backend/lca-lite-service/README.md)

