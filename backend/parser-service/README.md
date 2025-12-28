# Parser Service - EcoLabel-MS

Service d'extraction et parsing de données produits pour la plateforme EcoLabel-MS.

## 🎯 Fonctionnalités

- **OCR** : Extraction de texte depuis images avec Tesseract
- **Parsing PDF** : Extraction de texte depuis fichiers PDF
- **Parsing HTML** : Extraction structurée depuis pages HTML
- **Codes-barres** : Détection et validation de GTIN
- **Nettoyage texte** : Normalisation et extraction d'informations structurées
- **Base de données** : Stockage PostgreSQL des métadonnées produits

## 🏗️ Architecture

```
parser-service/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration
│   ├── models.py               # Modèles SQLAlchemy
│   ├── schemas.py              # Modèles Pydantic
│   ├── database.py             # Connexion DB
│   ├── ocr/                    # Services OCR
│   ├── parsers/                # Parsers (PDF, HTML, Image)
│   ├── extractors/             # Extracteurs (GTIN, texte)
│   └── utils/                  # Utilitaires
├── tests/                      # Tests unitaires
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🚀 Installation

### Prérequis

- Python 3.11+
- PostgreSQL 15+
- Tesseract OCR
- Docker & Docker Compose (optionnel)

### Installation locale

1. **Installer Tesseract OCR** :
```bash
# macOS
brew install tesseract tesseract-lang

# Ubuntu/Debian
sudo apt-get install tesseract-ocr tesseract-ocr-fra tesseract-ocr-eng

# Windows
# Télécharger depuis: https://github.com/UB-Mannheim/tesseract/wiki
```

2. **Installer les dépendances Python** :
```bash
cd parser-service
pip install -r requirements.txt
```

3. **Configurer la base de données** :
```bash
# Créer un fichier .env
cp .env.example .env
# Éditer .env avec vos paramètres
```

4. **Lancer le service** :
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

### Installation avec Docker

```bash
docker-compose up -d
```

Le service sera accessible sur `http://localhost:8001`

## 📡 API Endpoints

### Health Check
```
GET /health
```

### Parse un lot de fichiers
```
POST /product/parse
Content-Type: multipart/form-data

Body: files[] (PDF, HTML, JPG, PNG)
```

### Parse un seul fichier
```
POST /product/parse/single
Content-Type: multipart/form-data

Body: file (PDF, HTML, JPG, PNG)
```

### Récupérer un produit
```
GET /product/{product_id}
```

## 📝 Exemple d'utilisation

### Avec curl

```bash
# Parse un fichier image
curl -X POST "http://localhost:8001/product/parse/single" \
  -F "file=@/path/to/product_image.jpg"

# Parse plusieurs fichiers
curl -X POST "http://localhost:8001/product/parse" \
  -F "files=@/path/to/file1.pdf" \
  -F "files=@/path/to/file2.jpg"
```

### Avec Python

```python
import requests

url = "http://localhost:8001/product/parse/single"
files = {"file": open("product.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## 🧪 Tests

```bash
# Installer pytest
pip install pytest pytest-asyncio

# Lancer les tests
pytest tests/
```

## 🔧 Configuration

Variables d'environnement (`.env`) :

- `DATABASE_URL` : URL de connexion PostgreSQL
- `TESSERACT_CMD` : Chemin vers l'exécutable Tesseract
- `TESSERACT_LANG` : Langues OCR (ex: `fra+eng`)
- `UPLOAD_DIR` : Dossier temporaire pour les uploads
- `MAX_FILE_SIZE` : Taille max fichier (bytes)

## 📦 Formats supportés

- **Images** : JPG, JPEG, PNG, BMP, TIFF
- **Documents** : PDF
- **Web** : HTML, HTM

## 🔍 Extraction d'informations

Le service extrait automatiquement :

- **GTIN** : Code-barres (EAN-8, EAN-13, UPC, etc.)
- **Nom produit** : Depuis texte ou HTML
- **Ingrédients** : Liste d'ingrédients normalisée
- **Emballage** : Informations d'emballage
- **Métadonnées** : Type fichier, taille, confiance OCR

## 🐛 Dépannage

### Erreur Tesseract non trouvé
```bash
# Vérifier l'installation
tesseract --version

# Définir le chemin dans .env
TESSERACT_CMD=/usr/bin/tesseract
```

### Erreur de connexion PostgreSQL
```bash
# Vérifier que PostgreSQL est démarré
# Vérifier les credentials dans .env
```

### Erreur de mémoire
```bash
# Réduire MAX_FILE_SIZE dans .env
# Ou augmenter les ressources Docker
```

## 📄 Licence

Propriétaire - EcoLabel-MS

