# Dépannage SonarQube - Erreur d'authentification

## Vérifications à faire

### 1. Vérifier que le token est bien sélectionné dans Jenkins

1. **Manage Jenkins** → **Configure System**
2. Section **"SonarQube servers"**
3. Vérifier que :
   - **Name** : `SonarQube` (exactement)
   - **Server URL** : `http://localhost:9000`
   - **Server authentication token** : Le menu déroulant doit afficher **"SonarQube token for CI/CD"** (pas vide !)
4. Si le menu est vide ou ne montre pas le token, **sélectionner le token** et cliquer sur **"Save"**

### 2. Vérifier que le token est valide dans SonarQube

1. Ouvrir SonarQube : http://localhost:9000
2. Cliquer sur l'icône **"A"** → **My Account**
3. Onglet **Security**
4. Vérifier que le token **"jenkins-ci-cd"** existe
5. Si le token n'existe pas ou a été supprimé, créer un nouveau token :
   - **Name** : `jenkins-ci-cd`
   - Cliquer sur **"Generate"**
   - **Copier le token** (commence par `squ_...`)
6. Mettre à jour le credential dans Jenkins :
   - **Manage Jenkins** → **Credentials** → **System** → **Global credentials**
   - Trouver **"SonarQube token for CI/CD"**
   - Cliquer dessus → **"Update"**
   - Cliquer sur **"Change Password"**
   - Coller le nouveau token
   - **Save**

### 3. Vérifier les logs Jenkins

Dans les logs du stage "Code Quality - SonarQube", chercher :
- `Token configured: squ_...` → Le token est bien passé
- `ERROR: SONAR_TOKEN is not set!` → Le token n'est pas configuré
- `Not authorized` → Le token est invalide ou expiré

### 4. Solution alternative : Utiliser directement le token

Si le problème persiste, on peut définir le token directement dans les variables d'environnement :

1. **Manage Jenkins** → **Configure System**
2. Section **"Global properties"**
3. Cocher **"Environment variables"**
4. Ajouter :
   - **Name** : `SONAR_TOKEN`
   - **Value** : Votre token SonarQube (commence par `squ_...`)
5. **Save**

## Erreurs courantes

### "Not authorized"
- **Cause** : Token invalide, expiré, ou non configuré
- **Solution** : Créer un nouveau token dans SonarQube et le mettre à jour dans Jenkins

### "SONAR_TOKEN is not set!"
- **Cause** : Le token n'est pas configuré dans Jenkins
- **Solution** : Configurer le token dans "SonarQube servers" ou dans "Global properties"

### "Failed to query server version"
- **Cause** : SonarQube n'est pas accessible
- **Solution** : Vérifier que SonarQube est en cours d'exécution : `docker ps | grep sonarqube`

