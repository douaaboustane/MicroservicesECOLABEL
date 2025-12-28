"""
Utilitaires pour la gestion des fichiers
"""
import os
import json
import csv
import pandas as pd
from pathlib import Path
from typing import Union, List, Dict, Any


def ensure_dir(directory: Union[str, Path]):
    """Crée un dossier s'il n'existe pas"""
    Path(directory).mkdir(parents=True, exist_ok=True)


def save_json(data: Union[Dict, List], filepath: Union[str, Path]):
    """Sauvegarde des données en JSON"""
    ensure_dir(Path(filepath).parent)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(filepath: Union[str, Path]) -> Union[Dict, List]:
    """Charge des données depuis JSON"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_csv(data: List[Dict], filepath: Union[str, Path]):
    """Sauvegarde des données en CSV"""
    ensure_dir(Path(filepath).parent)
    if data:
        keys = data[0].keys()
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)


def load_csv(filepath: Union[str, Path]) -> List[Dict]:
    """Charge des données depuis CSV"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def save_dataframe(df: pd.DataFrame, filepath: Union[str, Path], compression='gzip'):
    """Sauvegarde un DataFrame avec compression"""
    ensure_dir(Path(filepath).parent)
    
    if filepath.endswith('.csv') or filepath.endswith('.csv.gz'):
        df.to_csv(filepath, index=False, compression=compression if compression else None)
    elif filepath.endswith('.parquet'):
        df.to_parquet(filepath, compression=compression, index=False)
    elif filepath.endswith('.json') or filepath.endswith('.jsonl'):
        df.to_json(filepath, orient='records', lines=filepath.endswith('.jsonl'), force_ascii=False)
    else:
        raise ValueError(f"Format non supporté: {filepath}")


def load_dataframe(filepath: Union[str, Path]) -> pd.DataFrame:
    """Charge un DataFrame depuis divers formats"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Fichier introuvable: {filepath}")
    
    filepath_str = str(filepath)
    
    if filepath_str.endswith('.csv') or filepath_str.endswith('.csv.gz'):
        # Détecter automatiquement la compression
        try:
            # Essayer d'abord avec compression='infer' (détecte automatiquement)
            return pd.read_csv(filepath, compression='infer')
        except UnicodeDecodeError:
            # Si erreur, essayer avec compression='gzip'
            return pd.read_csv(filepath, compression='gzip')
    elif filepath_str.endswith('.parquet'):
        return pd.read_parquet(filepath)
    elif filepath_str.endswith('.json'):
        return pd.read_json(filepath)
    elif filepath_str.endswith('.jsonl'):
        return pd.read_json(filepath, lines=True)
    else:
        raise ValueError(f"Format non supporté: {filepath}")


def get_file_size(filepath: Union[str, Path]) -> str:
    """Retourne la taille d'un fichier formatée"""
    size_bytes = os.path.getsize(filepath)
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.2f} TB"


def list_files(directory: Union[str, Path], extension: str = None) -> List[Path]:
    """Liste les fichiers d'un dossier"""
    path = Path(directory)
    if not path.exists():
        return []
    
    if extension:
        return list(path.glob(f"*.{extension}"))
    else:
        return [f for f in path.iterdir() if f.is_file()]

