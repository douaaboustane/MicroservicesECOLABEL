#!/bin/bash
set -e

SERVICE_NAME=$1
SERVICE_DIR="backend/${SERVICE_NAME}"

if [ -z "$SERVICE_NAME" ]; then
    echo "Error: Service name is required"
    echo "Usage: $0 <service-name>"
    exit 1
fi

echo "=== Testing ${SERVICE_NAME} ==="

if [ ! -d "${SERVICE_DIR}" ]; then
    echo "Error: Directory ${SERVICE_DIR} does not exist"
    exit 1
fi

cd "${SERVICE_DIR}"

# Créer un environnement virtuel
echo "Creating virtual environment..."
python3 -m venv venv || python -m venv venv
source venv/bin/activate || . venv/bin/activate || . venv/Scripts/activate

# Installer les dépendances
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install pytest pytest-cov || true

# Exécuter les tests
if [ -d "tests" ] && [ "$(ls -A tests 2>/dev/null)" ]; then
    echo "Running tests for ${SERVICE_NAME}..."
    pytest tests/ -v --cov=app --cov-report=xml --cov-report=html || {
        echo "WARNING: Some tests failed for ${SERVICE_NAME}"
        exit_code=$?
    }
else
    echo "WARNING: No tests found for ${SERVICE_NAME}"
    exit_code=0
fi

# Nettoyer
deactivate || true
rm -rf venv || true

echo "Testing completed for ${SERVICE_NAME}"
exit ${exit_code:-0}

