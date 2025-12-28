import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../../../core/constants/colors.dart';
import '../../../history/presentation/history_providers.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Widget avec graphiques de statistiques utilisant fl_chart
class StatisticsCharts extends ConsumerWidget {
  const StatisticsCharts({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final historyItems = ref.watch(historyControllerProvider);
    
    // Données pour le graphique d'évolution (7 derniers jours)
    final evolutionData = _getEvolutionData(historyItems);
    
    // Données pour la répartition des scores
    final scoreDistribution = _getScoreDistribution(historyItems);
    
    // Données pour l'impact
    final impactData = _getImpactData(historyItems);

    return Column(
      children: [
        // Graphique d'évolution
        _buildEvolutionChart(evolutionData),
        const SizedBox(height: 16),
        
        // Répartition des scores
        _buildScoreDistributionChart(scoreDistribution),
        const SizedBox(height: 16),
        
        // Impact détaillé
        _buildImpactCharts(impactData),
      ],
    );
  }

  List<FlSpot> _getEvolutionData(List historyItems) {
    // Simuler des données pour les 7 derniers jours
    final now = DateTime.now();
    final spots = <FlSpot>[];
    
    for (int i = 6; i >= 0; i--) {
      final date = now.subtract(Duration(days: i));
      // Calculer le score moyen pour ce jour (simplifié)
      final dayItems = historyItems.where((item) {
        final itemDate = item.scannedAt;
        return itemDate.year == date.year &&
            itemDate.month == date.month &&
            itemDate.day == date.day;
      }).toList();
      
      double avgScore = 0;
      if (dayItems.isNotEmpty) {
        final scores = dayItems
            .where((item) => item.scoreNumeric != null)
            .map((item) => item.scoreNumeric!.toDouble())
            .toList();
        if (scores.isNotEmpty) {
          avgScore = scores.reduce((a, b) => a + b) / scores.length;
        }
      } else {
        // Valeur par défaut si pas de données
        avgScore = 50 + (i * 5).toDouble();
      }
      
      spots.add(FlSpot((6 - i).toDouble(), avgScore));
    }
    
    return spots;
  }

  Map<String, int> _getScoreDistribution(List historyItems) {
    final distribution = <String, int>{'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0};
    
    for (final item in historyItems) {
      if (item.scoreLetter != null && distribution.containsKey(item.scoreLetter)) {
        distribution[item.scoreLetter!] = (distribution[item.scoreLetter] ?? 0) + 1;
      }
    }
    
    return distribution;
  }

  Map<String, double> _getImpactData(List historyItems) {
    final total = historyItems.length;
    return {
      'CO₂': (total * 0.5).clamp(0.0, 100.0),
      'Eau': (total * 18.75).clamp(0.0, 100.0),
      'Énergie': (total * 1.6).clamp(0.0, 100.0),
    };
  }

  Widget _buildEvolutionChart(List<FlSpot> spots) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Évolution du score (7 derniers jours)',
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            color: Colors.grey[700],
          ),
        ),
        const SizedBox(height: 12),
        SizedBox(
          height: 180,
          child: LineChart(
            LineChartData(
              gridData: FlGridData(
                show: true,
                drawVerticalLine: false,
                horizontalInterval: 20,
                getDrawingHorizontalLine: (value) {
                  return FlLine(
                    color: Colors.grey[200]!,
                    strokeWidth: 1,
                  );
                },
              ),
              titlesData: FlTitlesData(
                show: true,
                rightTitles: const AxisTitles(
                  sideTitles: SideTitles(showTitles: false),
                ),
                topTitles: const AxisTitles(
                  sideTitles: SideTitles(showTitles: false),
                ),
                bottomTitles: AxisTitles(
                  sideTitles: SideTitles(
                    showTitles: true,
                    reservedSize: 30,
                    interval: 1,
                    getTitlesWidget: (value, meta) {
                      final days = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];
                      if (value.toInt() >= 0 && value.toInt() < days.length) {
                        return Text(
                          days[value.toInt()],
                          style: TextStyle(
                            color: Colors.grey[600],
                            fontSize: 10,
                          ),
                        );
                      }
                      return const Text('');
                    },
                  ),
                ),
                leftTitles: AxisTitles(
                  sideTitles: SideTitles(
                    showTitles: true,
                    reservedSize: 40,
                    interval: 20,
                    getTitlesWidget: (value, meta) {
                      return Text(
                        value.toInt().toString(),
                        style: TextStyle(
                          color: Colors.grey[600],
                          fontSize: 10,
                        ),
                      );
                    },
                  ),
                ),
              ),
              borderData: FlBorderData(
                show: true,
                border: Border(
                  bottom: BorderSide(color: Colors.grey[300]!),
                  left: BorderSide(color: Colors.grey[300]!),
                ),
              ),
              minX: 0,
              maxX: 6,
              minY: 0,
              maxY: 100,
              lineBarsData: [
                LineChartBarData(
                  spots: spots,
                  isCurved: true,
                  color: EcoColors.primaryGreen,
                  barWidth: 3,
                  isStrokeCapRound: true,
                  dotData: FlDotData(
                    show: true,
                    getDotPainter: (spot, percent, barData, index) {
                      return FlDotCirclePainter(
                        radius: 4,
                        color: EcoColors.primaryGreen,
                        strokeWidth: 2,
                        strokeColor: Colors.white,
                      );
                    },
                  ),
                  belowBarData: BarAreaData(
                    show: true,
                    color: EcoColors.primaryGreen.withValues(alpha: 0.1),
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildScoreDistributionChart(Map<String, int> distribution) {
    final total = distribution.values.reduce((a, b) => a + b);
    if (total == 0) {
      return const SizedBox.shrink();
    }

    final colors = {
      'A': EcoColors.scoreA,
      'B': EcoColors.scoreB,
      'C': EcoColors.scoreC,
      'D': EcoColors.scoreD,
      'E': EcoColors.scoreE,
    };

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Répartition des scores',
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            color: Colors.grey[700],
          ),
        ),
        const SizedBox(height: 12),
        ...distribution.entries.map<Widget>((entry) {
          final percentage = total > 0 ? (entry.value / total * 100) : 0.0;
          final color = colors[entry.key] ?? Colors.grey;
          
          return Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'Score ${entry.key}',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w600,
                        color: Colors.grey[700],
                      ),
                    ),
                    Text(
                      '${percentage.toStringAsFixed(0)}%',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        color: color,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 4),
                ClipRRect(
                  borderRadius: BorderRadius.circular(4),
                  child: LinearProgressIndicator(
                    value: percentage / 100,
                    minHeight: 8,
                    backgroundColor: Colors.grey[200],
                    valueColor: AlwaysStoppedAnimation<Color>(color),
                  ),
                ),
              ],
            ),
          );
        }).toList(),
      ],
    );
  }

  Widget _buildImpactCharts(Map<String, double> impactData) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Impact détaillé',
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            color: Colors.grey[700],
          ),
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            Expanded(
              child: _buildCircularProgress(
                'CO₂',
                impactData['CO₂'] ?? 0.0,
                EcoColors.co2Color,
                '12kg',
              ),
            ),
            Expanded(
              child: _buildCircularProgress(
                'Eau',
                impactData['Eau'] ?? 0.0,
                EcoColors.waterColor,
                '450L',
              ),
            ),
            Expanded(
              child: _buildCircularProgress(
                'Énergie',
                impactData['Énergie'] ?? 0.0,
                EcoColors.energyColor,
                '32kWh',
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildCircularProgress(
    String label,
    double progress,
    Color color,
    String value,
  ) {
    return Column(
      children: [
        SizedBox(
          width: 70,
          height: 70,
          child: Stack(
            alignment: Alignment.center,
            children: [
              SizedBox(
                width: 70,
                height: 70,
                child: CircularProgressIndicator(
                  value: progress / 100,
                  strokeWidth: 8,
                  backgroundColor: color.withValues(alpha: 0.1),
                  valueColor: AlwaysStoppedAnimation<Color>(color),
                ),
              ),
              Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    value,
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.bold,
                      color: color,
                    ),
                  ),
                  Text(
                    '${progress.toStringAsFixed(0)}%',
                    style: TextStyle(
                      fontSize: 10,
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(
            fontSize: 11,
            color: Colors.grey[700],
          ),
        ),
      ],
    );
  }
}

