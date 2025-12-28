import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/styles.dart';
import '../widgets/trends_card.dart';
import '../widgets/top_ingredients_card.dart';
import '../widgets/bad_ingredients_card.dart';
import '../widgets/anomalies_card.dart';

class InsightsPage extends ConsumerWidget {
  const InsightsPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        height: double.infinity,
        decoration: BoxDecoration(
          gradient: EcoStyles.gradientBackground(
            EcoColors.primaryGreen,
            EcoColors.scientificBlue,
          ),
        ),
        child: SafeArea(
          child: CustomScrollView(
            slivers: [
              // App Bar
              SliverAppBar(
                expandedHeight: 120,
                floating: false,
                pinned: true,
                backgroundColor: Colors.transparent,
                elevation: 0,
                flexibleSpace: FlexibleSpaceBar(
                  title: const Text(
                    'Insights & Analytics',
                    style: TextStyle(
                      color: EcoColors.primaryGreen,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  background: Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topLeft,
                        end: Alignment.bottomRight,
                        colors: [
                          EcoColors.primaryGreen.withOpacity(0.1),
                          EcoColors.scientificBlue.withOpacity(0.05),
                        ],
                      ),
                    ),
                  ),
                ),
              ),

              // Content
              SliverPadding(
                padding: const EdgeInsets.all(16),
                sliver: SliverList(
                  delegate: SliverChildListDelegate([
                    // Section 1: Tendances
                    TrendsCard(),
                    const SizedBox(height: 16),

                    // Section 2: Top Ingrédients
                    TopIngredientsCard(),
                    const SizedBox(height: 16),

                    // Section 3: Ingrédients à éviter
                    BadIngredientsCard(),
                    const SizedBox(height: 16),

                    // Section 4: Anomalies détectées
                    AnomaliesCard(),
                    const SizedBox(height: 32),
                  ]),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

