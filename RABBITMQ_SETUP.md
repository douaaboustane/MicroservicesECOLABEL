# 🐰 RabbitMQ - Configuration et Utilisation

## 📋 Vue d'ensemble

RabbitMQ a été intégré pour gérer les opérations asynchrones dans l'API Gateway. Au lieu d'utiliser FastAPI BackgroundTasks, les jobs sont maintenant publiés dans des queues RabbitMQ et traités par des workers dédiés.

## 🏗️ Architecture

```
Frontend
   ↓
API Gateway (Publie dans RabbitMQ)
   ↓
RabbitMQ Queue: product_scan
   ↓
Worker (Consomme et traite)
   ↓
Orchestrator (OCR → NLP → LCA → Scoring)
```

## 🚀 Démarrage

### 1. Démarrer RabbitMQ

```bash
docker-compose up -d rabbitmq
```

### 2. Vérifier que RabbitMQ est opérationnel

Accédez à l'interface de management :
👉 **http://localhost:15672**

- **Username**: `ecolabel`
- **Password**: `ecolabel123`

### 3. Démarrer tous les services

```bash
docker-compose up -d
```

Cela démarre :
- ✅ RabbitMQ
- ✅ API Gateway (publie dans RabbitMQ)
- ✅ API Gateway Worker (consomme et traite les jobs)

## 📊 Queues

Les queues suivantes sont créées automatiquement :

- `product_scan` : Jobs de scan de produit à traiter
- `ocr` : (Réservé pour futures optimisations)
- `nlp` : (Réservé pour futures optimisations)
- `lca` : (Réservé pour futures optimisations)
- `scoring` : (Réservé pour futures optimisations)

## 🔄 Workflow

### 1. Publication d'un job

Quand un utilisateur upload une image :

```python
# Dans app/routers/mobile.py
rabbitmq_service.publish_scan_job(
    job_id=job.id,
    image_data=image_data,
    filename=file.filename,
    user_id=user_id
)
```

### 2. Traitement par le worker

Le worker (`app/workers/job_worker.py`) :
1. Consomme le message de la queue `product_scan`
2. Décode l'image (base64)
3. Appelle l'orchestrator pour traiter le job
4. Met à jour le statut dans la base de données

### 3. Suivi du statut

Le frontend peut toujours interroger :
```
GET /mobile/products/scan/{job_id}/status
```

## 🛠️ Configuration

Les paramètres RabbitMQ sont dans `app/config.py` :

```python
RABBITMQ_HOST: str = "rabbitmq"
RABBITMQ_PORT: int = 5672
RABBITMQ_USER: str = "ecolabel"
RABBITMQ_PASSWORD: str = "ecolabel123"
RABBITMQ_VHOST: str = "/"
```

## 📈 Avantages de RabbitMQ

### vs FastAPI BackgroundTasks

✅ **Persistance** : Les jobs survivent aux redémarrages
✅ **Scalabilité** : Plusieurs workers peuvent traiter en parallèle
✅ **Monitoring** : Interface de management pour voir les queues
✅ **Fiabilité** : Messages persistants, retry automatique
✅ **Découplage** : API Gateway et Workers sont indépendants

## 🔍 Monitoring

### Interface de Management

Accédez à **http://localhost:15672** pour :
- Voir les queues et leur contenu
- Monitorer les messages publiés/consommés
- Voir les connexions et channels
- Gérer les exchanges et bindings

### Logs

```bash
# Logs du worker
docker-compose logs -f api-gateway-worker

# Logs de RabbitMQ
docker-compose logs -f rabbitmq

# Logs de l'API Gateway
docker-compose logs -f api-gateway
```

## 🧪 Test

1. **Tester la connexion RabbitMQ** :
```bash
docker-compose exec rabbitmq rabbitmq-diagnostics ping
```

2. **Vérifier les queues** :
```bash
docker-compose exec rabbitmq rabbitmqctl list_queues
```

3. **Tester le workflow complet** :
```bash
python test_workflow_complete.py <image_path>
```

## 🔧 Dépannage

### Worker ne démarre pas

Vérifiez que RabbitMQ est démarré :
```bash
docker-compose ps rabbitmq
```

### Messages non traités

Vérifiez les logs du worker :
```bash
docker-compose logs api-gateway-worker --tail 50
```

### Queue pleine

Augmentez le nombre de workers ou optimisez le traitement.

## 📝 Notes

- Les images sont encodées en base64 pour le transport via RabbitMQ
- Les messages sont persistants (survivent aux redémarrages)
- Le worker traite un message à la fois (QoS=1)
- En cas d'erreur, le message est réinséré dans la queue (requeue)

## 🚀 Prochaines étapes

- [ ] Implémenter des queues séparées pour chaque étape (OCR, NLP, LCA, Scoring)
- [ ] Ajouter des workers dédiés pour chaque étape
- [ ] Implémenter le retry avec backoff exponentiel
- [ ] Ajouter des métriques et monitoring avancé


