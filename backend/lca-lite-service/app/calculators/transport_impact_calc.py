"""
Calculateur d'impact pour le transport
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional

from app.config import settings
from app import schemas


class TransportImpactCalculator:
    """Calcule les impacts environnementaux du transport"""
    
    def __init__(self):
        self.factors_data = {}
        self.load_data()
    
    def load_data(self):
        """Charge les facteurs d'émission du transport"""
        try:
            file_path = Path(settings.TRANSPORT_FACTORS_FILE)
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.factors_data = json.load(f)
                print(f"✅ Facteurs transport chargés: {len(self.factors_data)} types")
            else:
                print(f"⚠️  Fichier transport introuvable: {file_path}")
        except Exception as e:
            print(f"❌ Erreur chargement transport: {e}")
    
    def calculate(self, transport: Optional[schemas.TransportInput], product_weight_kg: float = 1.0) -> Dict[str, Any]:
        """
        Calcule les impacts du transport.
        
        Args:
            transport: Informations sur le transport
            product_weight_kg: Poids du produit en kg
        
        Returns:
            Dictionnaire avec impacts
        """
        if not transport:
            return {
                "co2_kg": 0.0,
                "water_m3": 0.0,
                "energy_mj": 0.0,
                "acidification": 0.0,
                "eutrophisation": 0.0
            }
        
        # Déterminer le type de transport
        transport_type = transport.transport_type
        
        if not transport_type:
            # Déduire du pays d'origine/destination
            transport_type = self._infer_transport_type(
                transport.origin_country,
                transport.destination_country
            )
        
        # Déterminer la distance
        distance_km = transport.distance_km
        if distance_km is None:
            # Estimer selon les pays
            distance_km = self._estimate_distance(
                transport.origin_country,
                transport.destination_country
            )
        
        if distance_km is None or distance_km <= 0:
            distance_km = 500  # Distance par défaut
        
        # Récupérer les facteurs d'émission
        factors = self.factors_data.get(transport_type)
        if not factors:
            # Valeur par défaut (routier Europe)
            factors = {
                "co2_kg_per_tonne_km": 0.0006
            }
        
        # Calculer l'impact CO2 (kg CO2 / tonne.km)
        co2_per_tonne_km = factors.get("co2_kg_per_tonne_km", 0.0006)
        weight_tonnes = product_weight_kg / 1000.0
        
        impacts = {
            "co2_kg": co2_per_tonne_km * weight_tonnes * distance_km,
            "water_m3": 0.0,  # Transport n'utilise pas d'eau directement
            "energy_mj": 0.0,  # Calculable mais complexe, on se concentre sur CO2
            "acidification": 0.0,
            "eutrophisation": 0.0
        }
        
        return impacts
    
    def _infer_transport_type(self, origin: Optional[str], destination: Optional[str]) -> str:
        """Infère le type de transport selon les pays"""
        if not origin or not destination:
            return "routier_europe"
        
        # Si même pays
        if origin.upper() == destination.upper():
            if origin.upper() == "FR":
                return "routier_france"
            return "routier_europe"
        
        # Si pays européens
        europe_countries = ["FR", "DE", "ES", "IT", "BE", "NL", "PT", "AT", "CH"]
        if origin.upper() in europe_countries and destination.upper() in europe_countries:
            return "routier_europe"
        
        # Sinon, probablement aérien
        return "aerien"
    
    def _estimate_distance(self, origin: Optional[str], destination: Optional[str]) -> Optional[float]:
        """Estime la distance entre deux pays"""
        if not origin or not destination:
            return None
        
        # Distances approximatives (en km)
        distance_matrix = {
            ("FR", "FR"): 200,  # Distance moyenne en France
            ("FR", "ES"): 1000,
            ("FR", "IT"): 1200,
            ("FR", "DE"): 800,
            ("FR", "BE"): 300,
            ("ES", "FR"): 1000,
            ("IT", "FR"): 1200,
            ("DE", "FR"): 800,
            ("BE", "FR"): 300,
        }
        
        key = (origin.upper(), destination.upper())
        if key in distance_matrix:
            return distance_matrix[key]
        
        # Distance par défaut
        if origin.upper() == destination.upper():
            return 200  # Même pays
        else:
            return 1500  # Distance moyenne Europe

