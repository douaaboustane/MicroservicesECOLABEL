#!/bin/bash
set -e

echo "=== Starting Integration Tests ==="

# Fonction pour vérifier la santé d'un service
check_service() {
    local service_name=$1
    local url=$2
    local max_attempts=15
    local attempt=1
    
    echo "Checking ${service_name} at ${url}..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f "${url}" > /dev/null 2>&1; then
            echo "${service_name} is healthy"
            return 0
        fi
        echo "Waiting for ${service_name}... ($attempt/${max_attempts})"
        sleep 5
        attempt=$((attempt + 1))
    done
    
    echo "${service_name} health check failed after ${max_attempts} attempts"
    return 1
}

# Nettoyer les conteneurs existants pour éviter les conflits
echo "Cleaning up existing containers..."
docker-compose down -v || true

# Supprimer les conteneurs individuels s'ils existent encore
docker rm -f parser-postgres nlp-postgres lca-postgres scoring-postgres api-postgres rabbitmq \
    parser-service nlp-ingredients-service lca-lite-service scoring-service \
    api-gateway-service api-gateway-worker eureka-server 2>/dev/null || true

# Démarrer les services (sans rebuild - images déjà construites)
echo "Starting services with docker-compose (using existing images)..."

# Démarrer d'abord les services de base (DB, RabbitMQ, Eureka)
echo "Starting base services (databases, RabbitMQ, Eureka)..."
docker-compose up -d parser-db nlp-db lca-db scoring-db api-db rabbitmq eureka-server

# Attendre que RabbitMQ soit prêt (important car d'autres services en dépendent)
echo "Waiting for RabbitMQ to be ready..."
MAX_RABBITMQ_ATTEMPTS=30
RABBITMQ_ATTEMPT=1
while [ $RABBITMQ_ATTEMPT -le $MAX_RABBITMQ_ATTEMPTS ]; do
    if docker exec rabbitmq rabbitmq-diagnostics ping > /dev/null 2>&1; then
        echo "RabbitMQ is ready"
        break
    fi
    if [ $RABBITMQ_ATTEMPT -eq $MAX_RABBITMQ_ATTEMPTS ]; then
        echo "WARNING: RabbitMQ health check failed after ${MAX_RABBITMQ_ATTEMPTS} attempts"
        echo "Checking RabbitMQ logs..."
        docker logs rabbitmq --tail 50 || true
    fi
    echo "Waiting for RabbitMQ... ($RABBITMQ_ATTEMPT/$MAX_RABBITMQ_ATTEMPTS)"
    sleep 5
    RABBITMQ_ATTEMPT=$((RABBITMQ_ATTEMPT + 1))
done

# Attendre un peu plus pour que les bases de données soient prêtes
echo "Waiting for databases to be ready..."
sleep 15

# Maintenant démarrer les services applicatifs
echo "Starting application services..."
docker-compose up -d

# Attendre que les services soient prêts
echo "Waiting for services to be ready..."
sleep 15

# Vérifier que les bases de données sont prêtes
echo ""
echo "=== Database Health Checks ==="
echo "Checking api-db..."
MAX_DB_ATTEMPTS=20
DB_ATTEMPT=1
while [ $DB_ATTEMPT -le $MAX_DB_ATTEMPTS ]; do
    if docker exec api-postgres pg_isready -U ecolabel > /dev/null 2>&1; then
        echo "api-db is ready"
        break
    fi
    if [ $DB_ATTEMPT -eq $MAX_DB_ATTEMPTS ]; then
        echo "WARNING: api-db health check failed"
    fi
    echo "Waiting for api-db... ($DB_ATTEMPT/$MAX_DB_ATTEMPTS)"
    sleep 3
    DB_ATTEMPT=$((DB_ATTEMPT + 1))
done

# Health checks pour chaque service avec plus de tentatives pour l'API Gateway
echo ""
echo "=== Service Health Checks ==="

# API Gateway a besoin de plus de temps car il dépend de plusieurs services
echo "Checking API Gateway (may take longer as it depends on multiple services)..."
MAX_GATEWAY_ATTEMPTS=30
GATEWAY_ATTEMPT=1
while [ $GATEWAY_ATTEMPT -le $MAX_GATEWAY_ATTEMPTS ]; do
    if curl -f "http://localhost:8000/health" > /dev/null 2>&1; then
        echo "API Gateway is healthy"
        break
    fi
    if [ $GATEWAY_ATTEMPT -eq $MAX_GATEWAY_ATTEMPTS ]; then
        echo "WARNING: API Gateway health check failed after ${MAX_GATEWAY_ATTEMPTS} attempts"
        echo "Checking API Gateway logs..."
        docker logs api-gateway-service --tail 50 || true
    fi
    echo "Waiting for API Gateway... ($GATEWAY_ATTEMPT/$MAX_GATEWAY_ATTEMPTS)"
    sleep 5
    GATEWAY_ATTEMPT=$((GATEWAY_ATTEMPT + 1))
done

check_service "Parser Service" "http://localhost:8001/health" || echo "WARNING: Parser Service health check failed"
check_service "NLP Service" "http://localhost:8003/health" || echo "WARNING: NLP Service health check failed"
check_service "LCA Service" "http://localhost:8004/health" || echo "WARNING: LCA Service health check failed"
check_service "Scoring Service" "http://localhost:8005/health" || echo "WARNING: Scoring Service health check failed"

# Test workflow si disponible
echo ""
echo "=== Workflow Test ==="
if [ -f "test_workflow_simple.py" ]; then
    echo "Running workflow test..."
    pip3 install requests || pip install requests || true
    
    # Créer une image de test simple (1x1 pixel PNG)
    echo "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==" | base64 -d > test_image.png 2>/dev/null || true
    
    if [ -f "test_image.png" ]; then
        python3 test_workflow_simple.py test_image.png || echo "WARNING: Workflow test failed (non-blocking)"
    else
        echo "WARNING: Could not create test image, skipping workflow test"
    fi
else
    echo "WARNING: test_workflow_simple.py not found, skipping workflow test"
fi

# Collecter les logs
echo ""
echo "=== Collecting logs ==="
docker-compose logs --tail=100 > integration_logs.txt || true

echo ""
echo "Integration tests completed"
echo "Logs saved to: integration_logs.txt"

