"""
Script d'entraînement des modèles (point d'entrée depuis le dossier scripts)
"""
import sys
from pathlib import Path

# Ajouter le dossier app au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.train_models import main

if __name__ == "__main__":
    main()

