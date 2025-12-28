"""
Script d'entraînement avec données réelles (point d'entrée)
"""
import sys
from pathlib import Path

# Ajouter le dossier app au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.train_with_real_data import main

if __name__ == "__main__":
    main()

