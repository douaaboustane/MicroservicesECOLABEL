# EcoLabel-MS - Application Mobile Flutter

Application mobile Flutter moderne pour l'évaluation écologique des produits alimentaires.

## 🌱 Description

EcoLabel-MS permet aux utilisateurs de scanner ou uploader un produit, suivre l'état du traitement en temps réel, et consulter un score écologique détaillé et visuellement impactant.

## 🏗️ Architecture

L'application suit une architecture **Clean Architecture** avec séparation en couches :

```
lib/
├── core/                    # Code partagé
│   ├── config/             # Configuration (theme, routes, env)
│   ├── network/            # Client API et gestion réseau
│   ├── constants/          # Constantes (couleurs, typographie, strings)
│   ├── utils/              # Utilitaires
│   └── widgets/            # Widgets réutilisables
│
└── features/               # Fonctionnalités métier
    ├── scan/              # Scan de produits
    ├── processing/        # Suivi du traitement
    ├── result/            # Affichage des résultats
    └── history/           # Historique des scans
```

Chaque feature suit la structure :
- **presentation/** : Pages, widgets, controllers (Riverpod)
- **domain/** : Entités, repositories (interfaces), use cases
- **data/** : Modèles, datasources, implémentations des repositories

## 🎨 Design System

### Palette de couleurs

- **Vert primaire** : `#2E7D32` - Écologie
- **Vert clair** : `#66BB6A` - Succès / Score A
- **Bleu scientifique** : `#1565C0` - Science & fiabilité
- **Beige naturel** : `#F4F1EC` - Fond
- **Blanc cassé** : `#FAFAFA`

### Scores écologiques

- **A** : `#2E7D32` - Excellent
- **B** : `#7CB342` - Très bon
- **C** : `#FBC02D` - Moyen
- **D** : `#FB8C00` - Faible
- **E** : `#C62828` - Très faible

### Typographie

- **Titres** : Poppins (Bold)
- **Corps** : Inter (Regular)
- **Chiffres** : Inter (Semi-bold)

## 🚀 Installation

### Prérequis

- Flutter SDK (>=3.10.1)
- Dart SDK
- Android Studio / Xcode (pour les builds)

### Étapes

1. Installer les dépendances :
```bash
flutter pub get
```

2. Configurer l'URL de l'API backend dans `lib/core/config/env.dart` ou via variable d'environnement :
```bash
flutter run --dart-define=API_BASE_URL=http://localhost:8000
```

3. Lancer l'application :
```bash
flutter run
```

## 📱 Workflow de l'application

1. **Écran d'accueil** → CTA Scanner / Upload
2. **Scan/Upload** → Caméra ou galerie
3. **Prévisualisation** → Confirmation avant analyse
4. **Traitement** → Polling du statut (OCR → NLP → ACV → Score)
5. **Résultat** → Score écologique + indicateurs d'impact
6. **Historique** → Liste des produits scannés

## 🔌 API Endpoints

L'application communique avec les endpoints suivants :

- `POST /mobile/products/scan` - Créer un job de scan
- `GET /mobile/jobs/{id}` - Récupérer le statut d'un job
- `GET /mobile/jobs/{id}/result` - Récupérer le résultat final

## 🛠️ Technologies

- **Flutter** : Framework UI
- **Riverpod** : State management
- **Dio** : Client HTTP
- **GetIt** : Injection de dépendances
- **Camera** : Accès caméra
- **Image Picker** : Sélection d'images
- **Lottie** : Animations
- **Google Fonts** : Typographie

## 📦 Dépendances principales

Voir `pubspec.yaml` pour la liste complète.

## 🧪 Tests

```bash
flutter test
```

## 📝 Notes

- L'application utilise Material 3
- Les animations Lottie doivent être ajoutées dans `assets/animations/`
- Les images doivent être ajoutées dans `assets/images/`
- Le polling des jobs se fait toutes les 2 secondes avec un timeout de 5 minutes

## 🔄 État du développement

✅ Architecture complète  
✅ Design system  
✅ Features principales (scan, processing, result, history)  
✅ Injection de dépendances  
⏳ Tests unitaires  
⏳ Animations Lottie  
⏳ Gestion d'erreurs avancée  
⏳ Cache local  

## 📄 Licence

Propriétaire - EcoLabel-MS
