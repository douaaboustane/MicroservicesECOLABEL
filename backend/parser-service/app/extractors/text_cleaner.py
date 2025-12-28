import re
from typing import List, Tuple, Optional


class TextCleaner:
    """Nettoie et normalise le texte extrait"""
    
    @staticmethod
    def clean(text: str) -> str:
        """Nettoie le texte brut"""
        if not text:
            return ""
        
        # Supprimer les caractères de contrôle
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        # Normaliser les espaces multiples
        text = re.sub(r'\s+', ' ', text)
        
        # Supprimer les espaces en début/fin
        text = text.strip()
        
        return text
    
    @staticmethod
    def extract_product_name(text: str) -> str:
        """Extrait le nom du produit depuis le texte"""
        # Chercher des patterns communs
        patterns = [
            r'(?:Produit|Product|Nom)[\s:]+([A-Z][^\n]{5,50})',
            r'^([A-Z][A-Za-z\s]{5,50})(?:\n|$)',
            r'([A-Z][A-Za-z\s]{5,50})(?:\s+Ingrédients)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                if len(name) > 5 and len(name) < 100:
                    return name
        
        # Prendre la première ligne significative
        lines = text.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 5 and len(line) < 100:
                # Vérifier que ce n'est pas une liste d'ingrédients
                if not any(keyword in line.lower() for keyword in ['ingrédient', 'ingredient', 'composition']):
                    return line
        
        return "Unknown Product"
    
    @staticmethod
    def extract_ingredients(text: str) -> str:
        """Extrait la liste d'ingrédients depuis le texte"""
        # Chercher le mot-clé "ingrédients"
        patterns = [
            r'(?:Ingrédients?|Ingredients?|Composition)[\s:]+(.+?)(?:\n\n|\n[A-Z]|$)',
            r'(?:Ingrédients?|Ingredients?)[\s:]+(.+?)(?:Allergènes|Allergens|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                ingredients = match.group(1).strip()
                # Nettoyer
                ingredients = re.sub(r'\s+', ' ', ingredients)
                return ingredients
        
        # Chercher une liste après ":" ou "•"
        lines = text.split('\n')
        in_ingredients_section = False
        ingredients_lines = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            if any(keyword in line_lower for keyword in ['ingrédient', 'ingredient', 'composition']):
                in_ingredients_section = True
                # Extraire ce qui suit le mot-clé
                match = re.search(r':\s*(.+)', line)
                if match:
                    ingredients_lines.append(match.group(1))
                continue
            
            if in_ingredients_section:
                if line.strip() and not line.strip().startswith(('Allergènes', 'Allergens', 'Valeurs')):
                    ingredients_lines.append(line.strip())
                else:
                    break
        
        if ingredients_lines:
            return ', '.join(ingredients_lines)
        
        return ""
    
    @staticmethod
    def extract_packaging_info(text: str) -> Optional[str]:
        """Extrait les informations d'emballage"""
        patterns = [
            r'(?:Emballage|Packaging|Conditionnement)[\s:]+(.+?)(?:\n\n|\n[A-Z]|$)',
            r'(?:Emballé|Packaged)[\s:]+(.+?)(?:\n|$)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None
    
    @staticmethod
    def split_into_sections(text: str) -> List[Tuple[str, str]]:
        """Divise le texte en sections (nom, ingrédients, etc.)"""
        sections = []
        
        # Sections à chercher
        section_keywords = {
            'product_name': ['produit', 'product', 'nom'],
            'ingredients': ['ingrédient', 'ingredient', 'composition'],
            'packaging': ['emballage', 'packaging', 'conditionnement'],
            'nutrition': ['nutrition', 'valeur', 'énergie'],
        }
        
        lines = text.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Vérifier si c'est un début de section
            for section_name, keywords in section_keywords.items():
                if any(keyword in line_lower for keyword in keywords):
                    # Sauvegarder la section précédente
                    if current_section and current_content:
                        sections.append((current_section, '\n'.join(current_content)))
                    
                    # Nouvelle section
                    current_section = section_name
                    current_content = [line]
                    break
            else:
                if current_section:
                    current_content.append(line)
        
        # Dernière section
        if current_section and current_content:
            sections.append((current_section, '\n'.join(current_content)))
        
        return sections

