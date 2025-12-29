# Configuration finale du token SonarQube

## Le problème

Le token SonarQube n'est pas accessible dans le pipeline Jenkins. Le message d'erreur indique : `SONAR_TOKEN is not set!`

## Solution : Configurer le token dans Jenkins

### Option 1 : Variables d'environnement globales (RECOMMANDÉ)

1. **Manage Jenkins** → **Configure System**
2. Section **"Global properties"**
3. Cocher **"Environment variables"**
4. Cliquer sur **"Add"**
5. Remplir :
   - **Name** : `SONAR_TOKEN`
   - **Value** : Votre token SonarQube (copier depuis SonarQube)
     - Pour obtenir le token : http://localhost:9000 → "A" → My Account → Security → Tokens
6. Cliquer sur **"Save"**

### Option 2 : Configuration SonarQube dans Jenkins

1. **Manage Jenkins** → **Configure System**
2. Section **"SonarQube servers"**
3. Vérifier/Configurer :
   - **Name** : `SonarQube` (doit correspondre exactement)
   - **Server URL** : `http://localhost:9000`
   - **Server authentication token** : Sélectionner **"SonarQube token for CI/CD"** dans le menu déroulant
4. Cliquer sur **"Save"**

## Vérification

Après avoir configuré le token :

1. Relancer un build Jenkins sur la branche `main`
2. Dans les logs du stage "Code Quality - SonarQube", vous devriez voir :
   - `Token configured: squ_...` (les 10 premiers caractères)
   - Pas d'erreur `SONAR_TOKEN is not set!`

## Si le problème persiste

1. Vérifier que le token est valide dans SonarQube
2. Vérifier que SonarQube est accessible : `curl http://localhost:9000/api/system/status`
3. Vérifier que SonarQube est en cours d'exécution : `docker ps | grep sonarqube`

