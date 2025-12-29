# Prochaines étapes SonarQube

## ✅ Étape 1 : Créer un token (IMPORTANT)

1. Dans SonarQube, cliquez sur l'icône **"A"** (en haut à droite) → **"My Account"**
2. Allez dans l'onglet **"Security"**
3. Dans la section **"Generate Tokens"** :
   - **Name** : `jenkins-ci-cd`
   - Cliquez sur **"Generate"**
4. **COPIEZ LE TOKEN** (il ne sera affiché qu'une seule fois !)
   - Exemple : `squ_1234567890abcdef1234567890abcdef12345678`

## 🔧 Étape 2 : Configurer Jenkins (Optionnel mais recommandé)

### Option A : Configuration via Jenkins UI

1. Ouvrir Jenkins : http://localhost:8080
2. **Manage Jenkins** → **Manage Plugins**
3. Onglet **"Available"** → Rechercher **"SonarQube Scanner"**
4. Cocher et **Installer** → Redémarrer Jenkins si demandé
5. **Manage Jenkins** → **Configure System**
6. Section **"SonarQube servers"** :
   - Cliquez sur **"Add SonarQube"**
   - **Name** : `SonarQube`
   - **Server URL** : `http://localhost:9000`
   - **Server authentication token** : Coller le token créé à l'étape 1
7. Cliquez sur **"Save"**

### Option B : Sans configuration Jenkins

Le pipeline fonctionnera, mais le Quality Gate automatique ne sera pas disponible.
Vous pouvez définir les variables d'environnement dans Jenkins :
- `SONAR_HOST_URL=http://localhost:9000`
- `SONAR_TOKEN=<votre-token>`

## 🧪 Étape 3 : Tester le pipeline

Une fois le token créé, vous pouvez :

1. **Tester manuellement** (optionnel) :
```bash
docker run --rm -v "${PWD}:/usr/src" -w /usr/src -e SONAR_HOST_URL="http://host.docker.internal:9000" -e SONAR_TOKEN="votre-token" sonarsource/sonar-scanner-cli:latest -Dsonar.projectKey=ecolabel-ms -Dsonar.sources=backend
```

2. **Lancer le pipeline Jenkins** sur la branche `main` :
   - Le stage "Code Quality - SonarQube" s'exécutera automatiquement
   - Le stage "Quality Gate" vérifiera la qualité du code

## 📊 Étape 4 : Voir les résultats

Après l'analyse, vous verrez dans SonarQube :
- **Bugs** détectés
- **Vulnérabilités** de sécurité
- **Code Smells** (problèmes de qualité)
- **Couverture de code** (si les tests génèrent des rapports de couverture)

## ⚠️ Note importante

Le warning sur la version inactive de SonarQube peut être ignoré pour le développement local.
Pour la production, il faudra mettre à jour vers une version active.

