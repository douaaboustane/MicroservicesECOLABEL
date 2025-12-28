#!/bin/bash
set -e

SERVICE_NAME=$1
IMAGE_TAG=${2:-latest}
REGISTRY=${3:-localhost:5000}
IMAGE_PREFIX=${4:-ecolabel}

if [ -z "$SERVICE_NAME" ]; then
    echo "Error: Service name is required"
    echo "Usage: $0 <service-name> [image-tag] [registry] [image-prefix]"
    exit 1
fi

echo "=== Building ${SERVICE_NAME} ==="

SERVICE_DIR="backend/${SERVICE_NAME}"

if [ ! -d "${SERVICE_DIR}" ]; then
    echo "Error: Directory ${SERVICE_DIR} does not exist"
    exit 1
fi

cd "${SERVICE_DIR}"

# Vérifier que Dockerfile existe
if [ ! -f "Dockerfile" ]; then
    echo "Error: Dockerfile not found in ${SERVICE_DIR}"
    exit 1
fi

# Build l'image
echo "Building Docker image..."
docker build -t ${IMAGE_PREFIX}-${SERVICE_NAME}:${IMAGE_TAG} .
docker tag ${IMAGE_PREFIX}-${SERVICE_NAME}:${IMAGE_TAG} ${IMAGE_PREFIX}-${SERVICE_NAME}:latest

# Tag pour le registry (si configuré)
if [ "${REGISTRY}" != "localhost:5000" ]; then
    echo "Tagging for registry ${REGISTRY}..."
    docker tag ${IMAGE_PREFIX}-${SERVICE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_PREFIX}-${SERVICE_NAME}:${IMAGE_TAG}
    docker tag ${IMAGE_PREFIX}-${SERVICE_NAME}:${IMAGE_TAG} ${REGISTRY}/${IMAGE_PREFIX}-${SERVICE_NAME}:latest
fi

echo "${SERVICE_NAME} image built successfully"
echo "   Image: ${IMAGE_PREFIX}-${SERVICE_NAME}:${IMAGE_TAG}"
if [ "${REGISTRY}" != "localhost:5000" ]; then
    echo "   Registry: ${REGISTRY}/${IMAGE_PREFIX}-${SERVICE_NAME}:${IMAGE_TAG}"
fi

