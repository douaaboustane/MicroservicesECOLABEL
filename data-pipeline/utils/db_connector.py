"""
Connecteur PostgreSQL
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import yaml
from pathlib import Path
from typing import Optional


class DatabaseConnector:
    """Gestion des connexions PostgreSQL"""
    
    def __init__(self, config_file: str = "config/database_config.yaml"):
        self.config = self._load_config(config_file)
        self.engine = None
        self.SessionLocal = None
    
    def _load_config(self, config_file: str) -> dict:
        """Charge la configuration depuis YAML"""
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)['database']
    
    def connect(self):
        """Établit la connexion à la base de données"""
        db_url = f"postgresql://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['name']}"
        
        self.engine = create_engine(
            db_url,
            pool_size=self.config.get('pool_size', 10),
            max_overflow=self.config.get('max_overflow', 20),
            pool_timeout=self.config.get('pool_timeout', 30),
            pool_recycle=self.config.get('pool_recycle', 3600),
        )
        
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
        return self.engine
    
    @contextmanager
    def get_session(self) -> Session:
        """Context manager pour les sessions"""
        if self.SessionLocal is None:
            self.connect()
        
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def execute_query(self, query: str, params: Optional[dict] = None):
        """Exécute une requête SQL"""
        with self.get_session() as session:
            result = session.execute(text(query), params or {})
            return result.fetchall()
    
    def bulk_insert(self, table: str, data: list):
        """Insert en masse dans une table"""
        if not data:
            return
        
        # TODO: Implémenter l'insert en masse avec pandas
        pass
    
    def test_connection(self) -> bool:
        """Teste la connexion à la base de données"""
        try:
            if self.engine is None:
                self.connect()
            
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Erreur de connexion: {e}")
            return False


# Instance globale
db = DatabaseConnector()

