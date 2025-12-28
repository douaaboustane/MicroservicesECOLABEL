import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/utils/date_utils.dart' as app_date_utils;
import '../../../../core/widgets/eco_card.dart';

/// Widget pour le header produit (identification)
class ProductHeaderCard extends StatelessWidget {
  final String? productImage;
  final String? productName;
  final DateTime scannedAt;
  final VoidCallback? onInfoPressed;

  const ProductHeaderCard({
    super.key,
    this.productImage,
    this.productName,
    required this.scannedAt,
    this.onInfoPressed,
  });

  @override
  Widget build(BuildContext context) {
    return EcoCard(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              // Image du produit
              if (productImage != null)
                ClipRRect(
                  borderRadius: BorderRadius.circular(12),
                  child: Image.network(
                    productImage!,
                    width: 80,
                    height: 80,
                    fit: BoxFit.cover,
                    errorBuilder: (context, error, stackTrace) => _buildPlaceholder(),
                  ),
                )
              else
                _buildPlaceholder(),
              const SizedBox(width: 16),
              // Nom et date
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      productName ?? 'Produit scanné',
                      style: EcoTypography.h3.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Row(
                      children: [
                        Icon(
                          Icons.calendar_today,
                          size: 14,
                          color: Colors.grey[600],
                        ),
                        const SizedBox(width: 4),
                        Text(
                          app_date_utils.DateUtils.formatRelative(scannedAt),
                          style: EcoTypography.bodySmall.copyWith(
                            color: Colors.grey[600],
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              // Icône info
              if (onInfoPressed != null)
                IconButton(
                  icon: const Icon(Icons.info_outline),
                  color: EcoColors.scientificBlue,
                  onPressed: onInfoPressed,
                ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildPlaceholder() {
    return Container(
      width: 80,
      height: 80,
      decoration: BoxDecoration(
        color: Colors.grey[200],
        borderRadius: BorderRadius.circular(12),
      ),
      child: Icon(
        Icons.image_outlined,
        color: Colors.grey[400],
        size: 40,
      ),
    );
  }
}
