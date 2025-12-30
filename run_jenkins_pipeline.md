# Guide d'exécution du Pipeline Jenkins

## Option 1 : Via l'Interface Web Jenkins (Recommandé)

### 1. Accéder à Jenkins
Ouvrez votre navigateur et allez à :
```
http://localhost:8080
```

### 2. Créer un Job Pipeline (si pas déjà créé)

1. Cliquez sur **"New Item"** dans le menu de gauche
2. Entrez un nom (ex: "EcoLabel-Pipeline")
3. Sélectionnez **"Pipeline"**
4. Cliquez sur **"OK"**

### 3. Configurer le Pipeline

Dans la configuration du job :

1. Dans la section **"Pipeline"** :
   - **Definition**: Sélectionnez **"Pipeline script from SCM"**
   - **SCM**: Sélectionnez **"Git"**
   - **Repository URL**: Entrez l'URL de votre dépôt Git (ou utilisez le chemin local)
   - **Script Path**: Entrez **"Jenkinsfile"**
   - **Branch**: **"*/main"** ou **"*/master"**

2. Cliquez sur **"Save"**

### 4. Lancer le Pipeline

1. Sur la page du job, cliquez sur **"Build Now"**
2. Le pipeline va s'exécuter
3. Cliquez sur le numéro de build pour voir les logs en temps réel

---

## Option 2 : Via l'API REST Jenkins

### Obtenir le Token API

1. Dans Jenkins : **Manage Jenkins** → **Users** → Cliquez sur votre utilisateur
2. Cliquez sur **"Configure"**
3. Dans **"API Token"**, cliquez sur **"Add new Token"**
4. Copiez le token généré

### Lancer le pipeline via curl

```powershell
# Remplacer JENKINS_USER, JENKINS_TOKEN et JOB_NAME
$user = "admin"
$token = "votre-token-api"
$jobName = "EcoLabel-Pipeline"

$auth = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("${user}:${token}"))
$headers = @{Authorization = "Basic $auth"}

Invoke-RestMethod -Uri "http://localhost:8080/job/$jobName/build" -Method Post -Headers $headers
```

---

## Option 3 : Exécuter les Scripts Manuellement

Si vous voulez tester les étapes individuellement sans Jenkins :

### Tests Unitaires
```powershell
# Pour chaque service
cd backend/parser-service
python -m pytest tests/ -v
```

### Tests d'Intégration
```powershell
# Depuis la racine du projet
bash jenkins/scripts/integration-test.sh
```

### Build Docker Images
```powershell
bash jenkins/scripts/build-image.sh parser-service
bash jenkins/scripts/build-image.sh nlp-ingredients-service
# etc...
```

---

## Option 4 : Utiliser Jenkins CLI

### Télécharger Jenkins CLI

```powershell
# Télécharger jenkins-cli.jar
Invoke-WebRequest -Uri "http://localhost:8080/jnlpJars/jenkins-cli.jar" -OutFile "jenkins-cli.jar"
```

### Lancer le pipeline

```powershell
java -jar jenkins-cli.jar -s http://localhost:8080 -auth admin:votre-token build EcoLabel-Pipeline
```

---

## Vérification de l'état

### Vérifier que Jenkins est actif
```powershell
docker ps --filter "name=jenkins"
```

### Voir les logs de Jenkins
```powershell
docker logs jenkins --tail 100 -f
```

### Accéder à l'interface web
```
http://localhost:8080
```

---

## Configuration nécessaire

### Variables d'environnement dans Jenkins

Pour que SonarQube fonctionne, configurez dans Jenkins :

**Manage Jenkins** → **Configure System** → **Global properties** → **Environment variables**

Ajoutez :
- `SONAR_TOKEN`: Votre token SonarQube
- `SONAR_HOST_URL`: http://localhost:9000 (ou host.docker.internal:9000)

---

## Dépannage

### Jenkins n'est pas accessible

1. Vérifier que le conteneur est démarré :
   ```powershell
   docker ps | findstr jenkins
   ```

2. Vérifier les ports :
   ```powershell
   docker port jenkins
   ```

3. Vérifier les logs :
   ```powershell
   docker logs jenkins
   ```

### Pipeline échoue

1. Vérifier les logs du build dans Jenkins UI
2. Vérifier que Docker est accessible depuis Jenkins
3. Vérifier que tous les services requis sont démarrés

### SonarQube non accessible

Si SonarQube est dans docker-compose.sonarqube.yml :
```powershell
docker-compose -f docker-compose.sonarqube.yml up -d
```

Puis dans Jenkins, utilisez `host.docker.internal:9000` au lieu de `localhost:9000`

