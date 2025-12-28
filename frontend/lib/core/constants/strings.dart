/// Constantes de chaînes de caractères pour EcoLabel-MS
class EcoStrings {
  // App
  static const String appName = 'EcoLabel';
  static const String appTagline = 'Votre impact environnemental en un scan';

  // Écran d'accueil
  static const String homeTitle = 'Scanner un produit';
  static const String homeSubtitle = 'Découvrez l\'impact écologique de vos produits alimentaires';
  static const String scanButton = 'Scanner';
  static const String uploadButton = 'Importer une image';

  // Scan
  static const String scanTitle = 'Scanner le produit';
  static const String scanSubtitle = 'Pointez la caméra vers l\'étiquette du produit';
  static const String previewTitle = 'Aperçu';
  static const String analyzeButton = 'Analyser le produit';

  // Traitement
  static const String processingTitle = 'Analyse en cours...';
  static const String processingSubtitle = 'Votre produit est en cours d\'évaluation';

  // Étapes de traitement
  static const String stepOcr = 'OCR';
  static const String stepOcrDesc = 'Reconnaissance du texte';
  static const String stepNlp = 'Extraction ingrédients';
  static const String stepNlpDesc = 'Analyse des ingrédients';
  static const String stepAcv = 'Calcul ACV';
  static const String stepAcvDesc = 'Analyse du cycle de vie';
  static const String stepScore = 'Calcul score';
  static const String stepScoreDesc = 'Génération du score final';

  // Résultat
  static const String resultTitle = 'Résultat';
  static const String scoreLabel = 'Score écologique';
  static const String impactLabel = 'Impact environnemental';
  static const String ingredientsLabel = 'Ingrédients détectés';
  static const String methodologyButton = 'Voir la méthodologie';

  // Historique
  static const String historyTitle = 'Historique';
  static const String historyEmpty = 'Aucun scan effectué';
  static const String historyEmptyDesc = 'Scannez votre premier produit pour commencer';

  // Erreurs
  static const String errorGeneric = 'Une erreur est survenue';
  static const String errorNetwork = 'Problème de connexion';
  static const String errorScan = 'Erreur lors du scan';
  static const String errorProcessing = 'Erreur lors du traitement';

  // Unités
  static const String unitCo2 = 'kg CO₂';
  static const String unitWater = 'L';
  static const String unitEnergy = 'kWh';
}
