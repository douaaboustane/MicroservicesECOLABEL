import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/widgets/eco_card.dart';

/// Page de méthodologie et transparence
class MethodologyPage extends StatelessWidget {
  const MethodologyPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: EcoColors.naturalBeige,
      appBar: AppBar(
        title: const Text('Méthodologie'),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Comment est calculé le score écologique ?',
              style: EcoTypography.h2.copyWith(
                color: EcoColors.primaryGreen,
              ),
            ),
            const SizedBox(height: 24),
            EcoCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '1. Reconnaissance du texte (OCR)',
                    style: EcoTypography.h4,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Extraction automatique du texte depuis l\'étiquette du produit grâce à la reconnaissance optique de caractères.',
                    style: EcoTypography.bodyMedium,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            EcoCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '2. Extraction des ingrédients (NLP)',
                    style: EcoTypography.h4,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Identification et extraction des ingrédients à partir du texte grâce au traitement du langage naturel.',
                    style: EcoTypography.bodyMedium,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            EcoCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '3. Analyse du cycle de vie (ACV)',
                    style: EcoTypography.h4,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Calcul de l\'impact environnemental de chaque ingrédient sur l\'ensemble de son cycle de vie : production, transformation, transport, emballage.',
                    style: EcoTypography.bodyMedium,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            EcoCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '4. Calcul du score final',
                    style: EcoTypography.h4,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Agrégation des impacts (CO₂, eau, énergie) selon vos préférences personnalisées pour générer un score global de A à E.',
                    style: EcoTypography.bodyMedium,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 32),
            Text(
              'Sources des données',
              style: EcoTypography.h3.copyWith(
                color: EcoColors.primaryGreen,
              ),
            ),
            const SizedBox(height: 16),
            EcoCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Base de données environnementales',
                    style: EcoTypography.h4,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '• Agribalyse (ADEME)\n• Ecoinvent\n• Base Carbone\n• Base IMPACTS',
                    style: EcoTypography.bodyMedium,
                  ),
                ],
              ),
            ),
            const SizedBox(height: 32),
            Text(
              'Version des modèles',
              style: EcoTypography.h3.copyWith(
                color: EcoColors.primaryGreen,
              ),
            ),
            const SizedBox(height: 16),
            EcoCard(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Modèles utilisés',
                    style: EcoTypography.h4,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    '• OCR: Tesseract v5.0\n• NLP: Modèle personnalisé v2.1\n• ACV: Méthodologie ISO 14040/14044\n• Score: Algorithme propriétaire v1.0',
                    style: EcoTypography.bodyMedium,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
