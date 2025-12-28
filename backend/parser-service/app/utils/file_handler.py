import os
import shutil
import aiofiles
from typing import Optional
from fastapi import UploadFile
from app.config import settings


class FileHandler:
    """Gestion des fichiers uploadés"""
    
    @staticmethod
    def ensure_upload_dir():
        """Crée le dossier d'upload s'il n'existe pas"""
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    @staticmethod
    def save_file(file: UploadFile, filename: Optional[str] = None) -> str:
        """
        Sauvegarde un fichier uploadé
        Returns: Chemin du fichier sauvegardé
        """
        FileHandler.ensure_upload_dir()
        
        if filename is None:
            filename = file.filename
        
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return file_path
    
    @staticmethod
    async def save_file_async(file: UploadFile, filename: Optional[str] = None) -> str:
        """
        Sauvegarde asynchrone d'un fichier
        """
        FileHandler.ensure_upload_dir()
        
        if filename is None:
            filename = file.filename
        
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        return file_path
    
    @staticmethod
    def delete_file(file_path: str):
        """Supprime un fichier"""
        if os.path.exists(file_path):
            os.remove(file_path)
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Retourne la taille d'un fichier en bytes"""
        return os.path.getsize(file_path)
    
    @staticmethod
    def validate_file_size(file_path: str) -> bool:
        """Valide que la taille du fichier est acceptable"""
        size = FileHandler.get_file_size(file_path)
        return size <= settings.MAX_FILE_SIZE
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """Retourne l'extension du fichier"""
        return filename.split('.')[-1].lower() if '.' in filename else ''
    
    @staticmethod
    def is_supported_format(filename: str) -> bool:
        """Vérifie si le format de fichier est supporté"""
        ext = FileHandler.get_file_extension(filename)
        supported = ['pdf', 'html', 'htm', 'jpg', 'jpeg', 'png', 'bmp', 'tiff']
        return ext in supported

