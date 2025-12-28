FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Télécharger le modèle spaCy français (optionnel - utilisé comme fallback uniquement)
# Le modèle NER personnalisé (ner_ingredients_v3) est prioritaire et devrait toujours être disponible
# Si le téléchargement échoue, ce n'est pas critique car le modèle personnalisé sera utilisé
# Note: Le téléchargement peut échouer mais ne bloque pas le build (|| true)
RUN python -m spacy download fr_core_news_md || true

# Copier le code de l'application
COPY ./app /app/app

# Créer le dossier pour les modèles
RUN mkdir -p /app/app/models

# Port d'exposition
EXPOSE 8003

# Lancer l'application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]

