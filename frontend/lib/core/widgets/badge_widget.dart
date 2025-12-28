import 'package:flutter/material.dart';
import '../constants/colors.dart';
import '../constants/typography.dart';

/// Widget pour afficher un badge/achievement avec état locked/unlocked
class BadgeWidget extends StatelessWidget {
  final String emoji;
  final String name;
  final bool isUnlocked;
  final String? unlockedDate;
  final VoidCallback? onTap;
  final Color? color;

  const BadgeWidget({
    super.key,
    required this.emoji,
    required this.name,
    this.isUnlocked = false,
    this.unlockedDate,
    this.onTap,
    this.color,
  });

  @override
  Widget build(BuildContext context) {
    final badgeColor = color ?? EcoColors.primaryGreen;

    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 80,
        height: 100,
        decoration: BoxDecoration(
          gradient: isUnlocked
              ? LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    badgeColor,
                    badgeColor.withValues(alpha: 0.7),
                  ],
                )
              : null,
          color: isUnlocked ? null : Colors.grey[300],
          borderRadius: BorderRadius.circular(16),
          boxShadow: isUnlocked
              ? [
                  BoxShadow(
                    color: badgeColor.withValues(alpha: 0.3),
                    blurRadius: 12,
                    offset: const Offset(0, 4),
                  ),
                ]
              : null,
        ),
        child: Stack(
          children: [
            // Content
            Padding(
              padding: const EdgeInsets.all(12),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    emoji,
                    style: const TextStyle(fontSize: 32),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    name,
                    style: EcoTypography.bodySmall.copyWith(
                      color: isUnlocked ? Colors.white : Colors.grey[600],
                      fontWeight: FontWeight.bold,
                      fontSize: 10,
                    ),
                    textAlign: TextAlign.center,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                  if (isUnlocked && unlockedDate != null) ...[
                    const SizedBox(height: 4),
                    Text(
                      unlockedDate!,
                      style: EcoTypography.caption.copyWith(
                        color: Colors.white.withValues(alpha: 0.8),
                        fontSize: 8,
                      ),
                    ),
                  ],
                ],
              ),
            ),

            // Lock overlay
            if (!isUnlocked)
              Container(
                decoration: BoxDecoration(
                  color: Colors.black.withValues(alpha: 0.3),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: const Center(
                  child: Icon(
                    Icons.lock,
                    color: Colors.white,
                    size: 24,
                  ),
                ),
              ),
          ],
        ),
      ),
    );
  }
}

