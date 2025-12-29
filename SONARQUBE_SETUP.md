# Configuration SonarQube pour Eco-projet

## Installation SonarQube

SonarQube est déjà téléchargé (images Docker présentes). Pour le démarrer :

```bash
# Démarrer SonarQube avec Docker Compose
docker-compose -f docker-compose.sonarqube.yml up -d

# Vérifier que SonarQube est accessible
curl http://localhost:9000/api/system/status
```

SonarQube sera accessible sur : **http://localhost:9000**

## Configuration initiale

1. **Premier accès** : Ouvrir http://localhost:9000
   - Login par défaut : `admin`
   - Mot de passe par défaut : `admin`
   - Vous serez invité à changer le mot de passe

2. **Créer un token** :
   - Aller dans : **My Account → Security → Generate Token**
   - Nom du token : `jenkins-ci-cd`
   - Copier le token généré

3. **Créer un projet** :
   - Aller dans : **Projects → Create Project → Manually**
   - Project Key : `ecolabel-ms`
   - Display Name : `EcoLabel Microservices`

## Configuration Jenkins

### Option 1 : Configuration via Jenkins UI (Recommandé)

1. **Installer le plugin SonarQube** :
   - Manage Jenkins → Manage Plugins → Available
   - Rechercher "SonarQube Scanner"
   - Installer et redémarrer Jenkins

2. **Configurer SonarQube Server** :
   - Manage Jenkins → Configure System
   - Section "SonarQube servers"
   - Ajouter un serveur :
     - Name : `SonarQube`
     - Server URL : `http://localhost:9000` (ou l'URL de votre SonarQube)
     - Server authentication token : Ajouter le token créé dans SonarQube

### Option 2 : Configuration via variables d'environnement

Dans Jenkins, ajouter des variables d'environnement :
- `SONAR_HOST_URL=http://localhost:9000`
- `SONAR_TOKEN=<votre-token>`

## Utilisation dans le Pipeline

Le pipeline Jenkins exécute SonarQube :
- **Quand** : Après les tests unitaires, avant le build des images
- **Sur quelle branche** : Uniquement sur `main`
- **Quality Gate** : Obligatoire - le pipeline échoue si la qualité n'est pas acceptable

## Structure du Pipeline

```
Checkout → Environment Setup → Unit Tests → [SonarQube] → Quality Gate → Build Docker Images → ...
```

## Fichiers de configuration

- `sonar-project.properties` : Configuration SonarQube pour le projet
- `docker-compose.sonarqube.yml` : Docker Compose pour démarrer SonarQube localement

## Exclusions d'analyse

Les fichiers suivants sont exclus de l'analyse SonarQube :
- `**/__pycache__/**`
- `**/tests/**`
- `**/venv/**`
- `**/node_modules/**`
- `**/models/**` (modèles ML)
- `**/data/**`
- `**/*.pyc`
- `**/migrations/**`
- `**/scripts/**`
- `**/test_*.py`

## Quality Gate

Le Quality Gate vérifie :
- **Bugs** : 0 bloquants
- **Vulnérabilités** : 0 critiques
- **Code Smells** : < 5% du code
- **Couverture** : > 80% (si disponible)

Si le Quality Gate échoue, le pipeline s'arrête et le déploiement est bloqué.

## Dépannage

### SonarQube n'est pas accessible

```bash
# Vérifier que SonarQube est en cours d'exécution
docker ps | grep sonarqube

# Démarrer SonarQube
docker-compose -f docker-compose.sonarqube.yml up -d

# Vérifier les logs
docker logs sonarqube
```

### Erreur "Quality Gate not found"

- Vérifier que le projet existe dans SonarQube
- Vérifier que le Project Key correspond (`ecolabel-ms`)
- Attendre quelques secondes après l'analyse pour que le Quality Gate soit calculé

### Erreur de connexion depuis Docker

Si SonarQube est sur le host et le scanner dans Docker :
- Utiliser `host.docker.internal:9000` au lieu de `localhost:9000`
- Ou utiliser `--network host` dans la commande docker run

## Prochaines étapes

1. Démarrer SonarQube : `docker-compose -f docker-compose.sonarqube.yml up -d`
2. Configurer dans Jenkins (voir section "Configuration Jenkins")
3. Lancer un build sur la branche `main` pour tester

