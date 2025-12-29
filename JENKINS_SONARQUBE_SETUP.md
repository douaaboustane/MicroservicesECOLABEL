# Configuration Jenkins pour SonarQube

## Étape 1 : Installer le plugin SonarQube dans Jenkins

1. Ouvrir Jenkins : **http://localhost:8080**
2. **Manage Jenkins** → **Manage Plugins**
3. Onglet **"Available"**
4. Rechercher : **"SonarQube Scanner"**
5. Cocher la case → Cliquer sur **"Install without restart"** ou **"Download now and install after restart"**
6. Si demandé, redémarrer Jenkins

## Étape 2 : Configurer SonarQube Server dans Jenkins

1. Dans Jenkins : **Manage Jenkins** → **Configure System**
2. Faire défiler jusqu'à la section **"SonarQube servers"**
3. Cliquer sur **"Add SonarQube"**
4. Remplir :
   - **Name** : `SonarQube`
   - **Server URL** : `http://localhost:9000`
   - **Server authentication token** : 
     - Cliquer sur **"Add"** → **"Jenkins"**
     - **Kind** : Secret text
     - **Secret** : Coller votre token SonarQube ici
     - **ID** : `sonar-token` (ou laisser vide)
     - **Description** : `SonarQube token for CI/CD`
     - Cliquer sur **"Add"**
     - Dans le menu déroulant, sélectionner le token que vous venez de créer
5. Cliquer sur **"Save"**

## Étape 3 : Vérifier la configuration

1. Retourner dans **Manage Jenkins** → **Configure System**
2. Vérifier que **"SonarQube"** apparaît dans la liste des serveurs
3. Vérifier que l'URL est correcte : `http://localhost:9000`

## Étape 4 : Tester le pipeline

1. Aller dans votre job Jenkins
2. Lancer un build sur la branche **`main`**
3. Le pipeline devrait maintenant :
   - Exécuter les tests unitaires
   - Lancer l'analyse SonarQube
   - Vérifier le Quality Gate
   - Continuer avec le build si tout est OK

## Alternative : Sans configuration Jenkins

Si vous ne configurez pas Jenkins, le pipeline utilisera Docker directement mais le Quality Gate automatique ne fonctionnera pas.

Dans ce cas, vous pouvez définir les variables d'environnement dans Jenkins :
- **Manage Jenkins** → **Configure System** → **Global properties**
- Cocher **"Environment variables"**
- Ajouter :
  - `SONAR_HOST_URL` = `http://localhost:9000`
  - `SONAR_TOKEN` = `<votre-token>`

