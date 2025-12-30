# Guide de Démonstration RabbitMQ

Ce guide explique comment démontrer l'utilisation de RabbitMQ dans votre projet.

## Prérequis

1. Tous les conteneurs Docker doivent être démarrés :
   ```powershell
   docker-compose ps
   ```

2. Vérifier que RabbitMQ est accessible :
   - UI: http://localhost:15672
   - Username: `ecolabel`
   - Password: `ecolabel123`

## Méthode 1 : Script Python (Recommandé)

### Utilisation basique
```powershell
python test_rabbitmq_demo.py
```

Le script cherchera automatiquement une image dans les chemins suivants :
- `C:\Users\doaa\Downloads\test_product.jpg`
- `C:\Users\doaa\Downloads\1.jpeg`
- `C:\Users\doaa\Downloads\a.jpeg`
- `C:\Users\doaa\Downloads\cerelac.png`
- `C:\Users\doaa\Downloads\coca.png`
- `C:\Users\doaa\Downloads\fanta.png`

### Utilisation avec une image spécifique
```powershell
python test_rabbitmq_demo.py "C:\chemin\vers\votre\image.jpg"
```

## Méthode 2 : Script PowerShell

```powershell
.\test_rabbitmq_demo.ps1
```

Ou avec une image spécifique :
```powershell
.\test_rabbitmq_demo.ps1 "C:\chemin\vers\votre\image.jpg"
```

## Méthode 3 : Curl (si installé sur Windows)

Si vous avez curl installé (Git Bash ou Windows 10+), vous pouvez utiliser :

```bash
curl -X POST "http://localhost:8000/mobile/products/scan" -F "file=@C:\Users\doaa\Downloads\1.jpeg"
```

**Note:** Sur Windows PowerShell, `curl` est un alias pour `Invoke-WebRequest` qui ne supporte pas la syntaxe `-F`. Utilisez les scripts Python ou PowerShell à la place.

## Observation dans RabbitMQ UI

### Étape 1 : Ouvrir RabbitMQ UI
1. Ouvrez votre navigateur : http://localhost:15672
2. Connectez-vous :
   - Username: `ecolabel`
   - Password: `ecolabel123`

### Étape 2 : Observer les queues

1. Cliquez sur l'onglet **"Queues and Streams"**

2. Vous devriez voir 5 queues :
   - `product_scan` (principale)
   - `ocr`
   - `nlp`
   - `lca`
   - `scoring`

### Étape 3 : Observer un message en temps réel

**Avant l'envoi :**
- Queue `product_scan` : **0 messages**

**Après l'envoi (immédiatement) :**
1. Cliquez sur la queue `product_scan`
2. Rafraîchissez la page
3. Vous devriez voir :
   - **Ready**: 1 (message en attente)
   - **Total**: augmente

**Pendant le traitement :**
- Le message peut passer à **Unacked** (si visible)
- Cela signifie que le worker est en train de le traiter

**Après traitement (quelques secondes) :**
- **Ready**: 0
- **Unacked**: 0
- **Total**: le nombre total de messages traités
- **Delivered**: augmente (message consommé avec succès)

## Vérifier le statut d'un job

Après avoir envoyé un message, vous recevrez un `job_id`. Pour vérifier le statut :

### Avec PowerShell
```powershell
$jobId = "votre-job-id-ici"
Invoke-RestMethod "http://localhost:8000/mobile/products/scan/$jobId/status"
```

### Avec Python
```python
import requests
job_id = "votre-job-id-ici"
response = requests.get(f"http://localhost:8000/mobile/products/scan/{job_id}/status")
print(response.json())
```

### Avec curl
```bash
curl http://localhost:8000/mobile/products/scan/votre-job-id-ici/status
```

## Points clés à démontrer

### 1. Architecture asynchrone
- L'API Gateway retourne immédiatement un `job_id`
- Le traitement se fait en arrière-plan via RabbitMQ
- Le client peut interroger le statut du job

### 2. Découplage des services
- Le message est publié dans RabbitMQ
- Le worker consomme le message indépendamment
- Les services sont découplés

### 3. Fiabilité
- Les messages sont persistants (durable queues)
- Les messages survivent aux redémarrages
- Les messages sont acquittés après traitement réussi

### 4. Scalabilité
- Plusieurs workers peuvent consommer la même queue
- Les messages sont distribués automatiquement
- Facile d'ajouter plus de workers pour gérer la charge

## Exemple de flux complet

1. **Envoi de la requête** :
   ```powershell
   python test_rabbitmq_demo.py
   ```
   Résultat : `Job ID: 8612831c-04ab-494b-9fb0-c76c6452c5ff`

2. **Observation dans RabbitMQ** :
   - Ouvrir http://localhost:15672
   - Queue `product_scan` → Voir le message apparaître

3. **Vérification du statut** :
   ```powershell
   Invoke-RestMethod "http://localhost:8000/mobile/products/scan/8612831c-04ab-494b-9fb0-c76c6452c5ff/status"
   ```

4. **Résultat attendu** :
   - Status passe de `PENDING` → `PROCESSING` → `DONE`
   - Les résultats intermédiaires apparaissent (parser_result, nlp_result, etc.)

## Dépannage

### Le message n'apparaît pas dans RabbitMQ
- Vérifier que l'API Gateway est démarré : `docker-compose ps`
- Vérifier les logs : `docker-compose logs api-gateway`

### Le message reste en "Ready" et n'est pas consommé
- Vérifier que le worker est démarré : `docker-compose ps api-gateway-worker`
- Vérifier les logs du worker : `docker-compose logs api-gateway-worker`

### Erreur de connexion
- Vérifier que RabbitMQ est démarré : `docker-compose ps rabbitmq`
- Vérifier que les services sont sur le même réseau Docker

