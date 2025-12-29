# Vérification rapide du token SonarQube

## Étape 1 : Vérifier dans Jenkins

1. **Manage Jenkins** → **Configure System**
2. Section **"SonarQube servers"**
3. Vérifier que le menu déroulant **"Server authentication token"** affiche bien **"SonarQube token for CI/CD"** (pas vide !)
4. Si c'est vide, **sélectionner le token** et cliquer sur **"Save"**

## Étape 2 : Vérifier dans SonarQube

1. Ouvrir http://localhost:9000
2. Cliquer sur **"A"** → **My Account** → **Security**
3. Vérifier que le token **"jenkins-ci-cd"** existe
4. Si le token n'existe pas, créer un nouveau token et le mettre à jour dans Jenkins

## Étape 3 : Solution rapide - Token direct

Si le problème persiste, définir le token directement :

1. **Manage Jenkins** → **Configure System**
2. **Global properties** → Cocher **"Environment variables"**
3. Ajouter :
   - **Name** : `SONAR_TOKEN`
   - **Value** : Votre token SonarQube (copier depuis SonarQube)
4. **Save**

