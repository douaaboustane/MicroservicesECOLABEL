# 📚 Guide d'Amélioration des Modèles de Scoring

Ce guide explique comment améliorer les modèles avec de vraies données labellisées.

## 🎯 État Actuel

Les modèles ont été entraînés avec :
- ✅ **Données réelles** : 1,988 produits Open Food Facts avec `ecoscore_grade`
- ⚠️ **Features estimées** : LCA et NLP sont estimés (pas réels)
- 📊 **Performance actuelle** :
  - Classification : 34% accuracy
  - Régression : R² = 0.03

## 🔧 Pourquoi les performances sont faibles ?

1. **LCA estimé** : Les impacts sont calculés avec des heuristiques, pas avec le vrai LCA Service
2. **NLP simplifié** : Extraction basique depuis texte, pas avec le vrai NLP Service
3. **Features limitées** : Certaines informations ne sont pas extraites correctement

## 🚀 Comment améliorer les modèles

### Option 1 : Utiliser les vrais services (Recommandé)

Pour avoir de meilleures features, il faut utiliser les vrais services :

```python
# 1. Appeler Parser Service pour extraire le texte
parser_result = await call_parser_service(image_file)

# 2. Appeler NLP Service pour extraire les ingrédients
nlp_result = await call_nlp_service(parser_result["ingredients_raw"])

# 3. Appeler LCA Service pour calculer les impacts réels
lca_result = await call_lca_service(nlp_result["ingredients"])

# 4. Utiliser ces vraies données pour entraîner
```

### Option 2 : Collecter plus de données

1. Scraper plus de produits Open Food Facts (10K+)
2. Filtrer ceux avec `ecoscore_grade` valide
3. Utiliser les données pour entraîner

### Option 3 : Utiliser les données Agribalyse

Les données Agribalyse ont des impacts réels :
- Utiliser `ef_score_mpt` comme proxy du score
- Utiliser les impacts réels (CO2, eau, énergie)

## 📝 Script d'entraînement amélioré

### Avec vraies données (via services)

```python
# Dans train_with_real_data.py, améliorer extract_features_from_product :

async def extract_features_with_services(self, product):
    # 1. Appeler NLP Service
    async with httpx.AsyncClient() as client:
        nlp_response = await client.post(
            f"{self.nlp_url}/nlp/extract",
            json={"text": product['ingredients_text']}
        )
        nlp_data = nlp_response.json()
    
    # 2. Appeler LCA Service
    lca_response = await client.post(
        f"{self.lca_url}/lca/calc",
        json={"ingredients": nlp_data['ingredients']}
    )
    lca_data = lca_response.json()
    
    # 3. Extraire features
    features = self.feature_extractor.extract(lca_data, nlp_data)
    return features
```

## 🔄 Workflow d'amélioration

1. **Collecter les données** :
   ```bash
   cd data-pipeline
   python 1_scrapers/openfoodfacts_scraper.py
   ```

2. **Nettoyer les données** :
   ```bash
   python 2_cleaning/normalizer.py
   ```

3. **Entraîner avec vraies données** :
   ```bash
   cd backend/scoring-service
   docker-compose exec scoring-service python -c "
   from app.services.train_with_real_data import RealDataTrainer
   trainer = RealDataTrainer()
   trainer.train_with_real_data('/tmp/products_cleaned.csv', max_samples=5000)
   "
   ```

4. **Évaluer les modèles** :
   - Vérifier les métriques
   - Tester sur des produits réels
   - Ajuster les hyperparamètres si nécessaire

## 📊 Métriques cibles

Pour des modèles de production :
- **Classification** : Accuracy > 70%, F1-Score > 0.70
- **Régression** : R² > 0.60, RMSE < 15

## 🎯 Prochaines étapes

1. ✅ Modèles entraînés avec données réelles (baseline)
2. ⏳ Améliorer l'extraction de features (utiliser vrais services)
3. ⏳ Collecter plus de données (10K+ produits)
4. ⏳ Fine-tuning des hyperparamètres
5. ⏳ Validation croisée
6. ⏳ Tests sur produits réels

## 💡 Astuces

- Utiliser `class_weight='balanced'` pour gérer les classes déséquilibrées
- Augmenter `n_estimators` pour meilleure précision (mais plus lent)
- Utiliser `GridSearchCV` pour trouver les meilleurs hyperparamètres
- Combiner données synthétiques + réelles pour plus de diversité

