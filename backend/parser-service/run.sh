#!/bin/bash

# Script de démarrage du Parser Service

echo "🚀 Démarrage du Parser Service..."

# Vérifier si .env existe
if [ ! -f .env ]; then
    echo "⚠️  Fichier .env non trouvé. Copie de env.example..."
    cp env.example .env
    echo "✅ Fichier .env créé. Veuillez le configurer avant de continuer."
    exit 1
fi

# Vérifier Tesseract
if ! command -v tesseract &> /dev/null; then
    echo "❌ Tesseract OCR n'est pas installé."
    echo "   Installation:"
    echo "   - macOS: brew install tesseract tesseract-lang"
    echo "   - Ubuntu: sudo apt-get install tesseract-ocr tesseract-ocr-fra tesseract-ocr-eng"
    exit 1
fi

# Créer le dossier d'upload
mkdir -p /tmp/uploads

# Lancer le service
echo "✅ Démarrage sur http://localhost:8001"
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

