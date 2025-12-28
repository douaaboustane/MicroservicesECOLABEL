# 📈 Plan d'Amélioration des Modèles

## ✅ Ce qui a été fait

1. ✅ Modèles entraînés avec données synthétiques (baseline)
2. ✅ Modèles entraînés avec données réelles Open Food Facts (1,988 produits)
3. ✅ Scripts d'entraînement créés
4. ✅ Service opérationnel avec modèles chargés

## ⚠️ Limitations actuelles

### Performance actuelle
- **Classification** : 34% accuracy (cible: >70%)
- **Régression** : R² = 0.03 (cible: >0.60)

### Causes principales
1. **Features LCA estimées** : Utilisation d'heuristiques au lieu du vrai LCA Service
2. **Features NLP simplifiées** : Extraction basique au lieu du vrai NLP Service
3. **Données limitées** : Seulement 1,988 échantillons

## 🎯 Plan d'amélioration

### Phase 1 : Améliorer l'extraction de features (Priorité 1)

**Objectif** : Utiliser les vrais services pour extraire les features

**Actions** :
1. Modifier `train_with_real_data.py` pour appeler les vrais services
2. Pour chaque produit :
   - Appeler NLP Service avec `ingredients_text`
   - Appeler LCA Service avec les ingrédients extraits
   - Utiliser les vraies données pour entraîner

**Code à ajouter** :
```python
async def extract_features_with_real_services(self, product):
    async with httpx.AsyncClient() as client:
        # NLP Service
        nlp_response = await client.post(
            f"{self.nlp_url}/nlp/extract",
            json={"text": product['ingredients_text']}
        )
        nlp_data = nlp_response.json()
        
        # LCA Service
        ingredients_for_lca = [
            {"name": ing["text"], "quantity_percentage": None}
            for ing in nlp_data.get("ingredients", [])
        ]
        
        lca_response = await client.post(
            f"{self.lca_url}/lca/calc",
            json={
                "ingredients": ingredients_for_lca,
                "packaging": {"type": nlp_data.get("packaging_type")},
                "product_weight_kg": 1.0
            }
        )
        lca_data = lca_response.json()
        
        # Extraire features
        return self._prepare_features(lca_data, nlp_data)
```

**Résultat attendu** : R² > 0.50, Accuracy > 60%

---

### Phase 2 : Collecter plus de données (Priorité 2)

**Objectif** : Augmenter le dataset à 10,000+ produits

**Actions** :
1. Scraper plus de produits Open Food Facts
2. Filtrer ceux avec `ecoscore_grade` valide
3. Ré-entraîner avec plus de données

**Commandes** :
```bash
cd data-pipeline
python 1_scrapers/openfoodfacts_scraper.py  # Scraper 10K+ produits
python 2_cleaning/normalizer.py
```

**Résultat attendu** : Meilleure généralisation

---

### Phase 3 : Fine-tuning des hyperparamètres (Priorité 3)

**Objectif** : Optimiser les hyperparamètres des modèles

**Actions** :
1. Utiliser `GridSearchCV` pour trouver les meilleurs paramètres
2. Tester différentes configurations :
   - `n_estimators`: [50, 100, 200, 300]
   - `max_depth`: [5, 10, 15, 20]
   - `min_samples_split`: [2, 5, 10]

**Code** :
```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [10, 15, 20],
    'min_samples_split': [2, 5, 10]
}

grid_search = GridSearchCV(
    RandomForestClassifier(class_weight='balanced'),
    param_grid,
    cv=5,
    scoring='f1_macro'
)
grid_search.fit(X_train, y_train)
```

**Résultat attendu** : +5-10% de performance

---

### Phase 4 : Validation et tests (Priorité 4)

**Objectif** : Valider les modèles sur des produits réels

**Actions** :
1. Créer un dataset de test avec produits réels
2. Comparer les prédictions avec les vrais scores
3. Analyser les erreurs
4. Ajuster si nécessaire

---

## 📊 Métriques de succès

| Métrique | Actuel | Cible Phase 1 | Cible Final |
|----------|--------|---------------|-------------|
| Classification Accuracy | 34% | 60% | 75% |
| Classification F1 | 0.34 | 0.60 | 0.75 |
| Régression R² | 0.03 | 0.50 | 0.70 |
| Régression RMSE | 28.37 | 20 | 15 |

---

## 🚀 Quick Start pour améliorer

### Étape 1 : Utiliser les vrais services

```bash
# Modifier train_with_real_data.py pour appeler les services
# Puis ré-entraîner
docker-compose exec scoring-service python -c "
from app.services.train_with_real_data import RealDataTrainer
trainer = RealDataTrainer()
trainer.train_with_real_data('/tmp/products_cleaned.csv', max_samples=3000)
"
```

### Étape 2 : Collecter plus de données

```bash
cd data-pipeline
python 1_scrapers/openfoodfacts_scraper.py  # Augmenter max_products à 10000
```

### Étape 3 : Ré-entraîner

```bash
docker-compose exec scoring-service python -c "
from app.services.train_with_real_data import RealDataTrainer
trainer = RealDataTrainer()
trainer.train_with_real_data('/tmp/products_cleaned.csv', max_samples=5000)
"
```

---

## 💡 Notes importantes

- Les modèles actuels fonctionnent mais peuvent être améliorés
- L'utilisation des vrais services (NLP + LCA) améliorera significativement les performances
- Plus de données = meilleure généralisation
- Les hyperparamètres peuvent être optimisés avec GridSearchCV

---

## 📝 Prochaines actions recommandées

1. **Immédiat** : Modifier `train_with_real_data.py` pour utiliser les vrais services
2. **Court terme** : Collecter 10K+ produits
3. **Moyen terme** : Fine-tuning des hyperparamètres
4. **Long terme** : Validation continue avec nouveaux produits

