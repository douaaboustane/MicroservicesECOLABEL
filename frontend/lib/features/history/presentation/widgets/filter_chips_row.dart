import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/typography.dart';

/// Row de chips pour filtrer par score
class FilterChipsRow extends StatelessWidget {
  final String? selectedFilter;
  final ValueChanged<String?> onFilterChanged;

  const FilterChipsRow({
    super.key,
    required this.selectedFilter,
    required this.onFilterChanged,
  });

  @override
  Widget build(BuildContext context) {
    final filters = [
      _FilterChip(label: 'Tous', value: null, color: EcoColors.primaryGreen),
      _FilterChip(label: 'A', value: 'A', color: EcoColors.scoreA),
      _FilterChip(label: 'B', value: 'B', color: EcoColors.scoreB),
      _FilterChip(label: 'C', value: 'C', color: EcoColors.scoreC),
      _FilterChip(label: 'D', value: 'D', color: EcoColors.scoreD),
      _FilterChip(label: 'E', value: 'E', color: EcoColors.scoreE),
    ];

    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: filters.map((filter) {
          final isSelected = selectedFilter == filter.value;
          return Padding(
            padding: const EdgeInsets.only(right: 8),
            child: _FilterChipWidget(
              label: filter.label,
              isSelected: isSelected,
              color: filter.color,
              onTap: () {
                HapticFeedback.selectionClick();
                onFilterChanged(filter.value);
              },
            ),
          );
        }).toList(),
      ),
    );
  }
}

class _FilterChip {
  final String label;
  final String? value;
  final Color color;

  const _FilterChip({
    required this.label,
    required this.value,
    required this.color,
  });
}

class _FilterChipWidget extends StatelessWidget {
  final String label;
  final bool isSelected;
  final Color color;
  final VoidCallback onTap;

  const _FilterChipWidget({
    required this.label,
    required this.isSelected,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        curve: Curves.easeInOut,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: isSelected ? color : Colors.white,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: isSelected ? color : Colors.grey[300]!,
            width: isSelected ? 0 : 1,
          ),
          boxShadow: isSelected
              ? [
                  BoxShadow(
                    color: color.withValues(alpha: 0.3),
                    blurRadius: 8,
                    offset: const Offset(0, 2),
                  ),
                ]
              : null,
        ),
        child: Text(
          label,
          style: EcoTypography.bodyMedium.copyWith(
            color: isSelected ? Colors.white : Colors.grey[700],
            fontWeight: isSelected ? FontWeight.bold : FontWeight.w600,
          ),
        ),
      ),
    );
  }
}

