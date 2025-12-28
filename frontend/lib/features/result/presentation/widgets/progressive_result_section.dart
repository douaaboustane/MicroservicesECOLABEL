import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/typography.dart';
import '../../../../core/widgets/eco_card.dart';

/// Widget pour la disclosure progressive (ne pas tout montrer d'un coup)
class ProgressiveResultSection extends StatefulWidget {
  final Widget child;
  final String title;
  final IconData icon;
  final bool initiallyExpanded;

  const ProgressiveResultSection({
    super.key,
    required this.child,
    required this.title,
    required this.icon,
    this.initiallyExpanded = false,
  });

  @override
  State<ProgressiveResultSection> createState() => _ProgressiveResultSectionState();
}

class _ProgressiveResultSectionState extends State<ProgressiveResultSection> {
  late bool _isExpanded;

  @override
  void initState() {
    super.initState();
    _isExpanded = widget.initiallyExpanded;
  }

  @override
  Widget build(BuildContext context) {
    return EcoCard(
      padding: EdgeInsets.zero,
      child: Column(
        children: [
          InkWell(
            onTap: () {
              setState(() {
                _isExpanded = !_isExpanded;
              });
            },
            borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                children: [
                  Icon(
                    widget.icon,
                    color: EcoColors.primaryGreen,
                    size: 24,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      widget.title,
                      style: EcoTypography.h4.copyWith(
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  Icon(
                    _isExpanded ? Icons.expand_less : Icons.expand_more,
                    color: EcoColors.primaryGreen,
                  ),
                ],
              ),
            ),
          ),
          if (_isExpanded)
            Padding(
              padding: const EdgeInsets.fromLTRB(20, 0, 20, 20),
              child: widget.child,
            ),
        ],
      ),
    );
  }
}


