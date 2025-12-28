import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/widgets/eco_card.dart';
import 'ingredient_chip.dart';

/// Section des ingrédients avec scroll horizontal
class IngredientsSection extends StatelessWidget {
  final List<String> ingredients;
  final List<String>? highImpactIngredients; // Ingrédients à fort impact

  const IngredientsSection({
    super.key,
    required this.ingredients,
    this.highImpactIngredients,
  });

  @override
  Widget build(BuildContext context) {
    if (ingredients.isEmpty) {
      return const SizedBox.shrink();
    }

    return EcoCard(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Ingrédients détectés',
            style: EcoTypography.h4,
          ),
          const SizedBox(height: 16),
          SizedBox(
            height: 40,
            child: ListView.separated(
              scrollDirection: Axis.horizontal,
              itemCount: ingredients.length,
              separatorBuilder: (context, index) => const SizedBox(width: 8),
              itemBuilder: (context, index) {
                final ingredient = ingredients[index];
                final isHighImpact = highImpactIngredients?.contains(ingredient) ?? false;
                return IngredientChip(
                  ingredient: ingredient,
                  isHighImpact: isHighImpact,
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
