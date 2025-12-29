# Vérifier que le token SonarQube est bien configuré

## Étape 1 : Vérifier la configuration SonarQube dans Jenkins

1. Dans Jenkins : **Manage Jenkins** → **Configure System**
2. Faire défiler jusqu'à la section **"SonarQube servers"**
3. Vérifier que :
   - **Name** : `SonarQube` (doit correspondre exactement au nom dans `withSonarQubeEnv('SonarQube')`)
   - **Server URL** : `http://localhost:9000`
   - **Server authentication token** : Le menu déroulant doit afficher **"SonarQube token for CI/CD"** ou **"sonar-token"**

## Étape 2 : Si le token n'est pas sélectionné

1. Dans le menu déroulant **"Server authentication token"**, cliquer dessus
2. Sélectionner **"SonarQube token for CI/CD"** (ou celui qui correspond à votre token)
3. Cliquer sur **"Save"**

## Étape 3 : Vérifier que le nom correspond

Dans le Jenkinsfile, on utilise :
```groovy
withSonarQubeEnv('SonarQube')
```

Le nom `'SonarQube'` doit correspondre **exactement** au **Name** dans la configuration SonarQube (pas l'ID du credential).

## Étape 4 : Alternative - Utiliser directement le credential

Si le problème persiste, on peut utiliser directement le credential par son ID :
- ID du token : `sonar-token` ou `sonar`

## Test

Après avoir vérifié la configuration, relancer un build Jenkins. Le token devrait maintenant être utilisé automatiquement.

