import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../constants/colors.dart';
import '../constants/typography.dart';

/// Item de navigation pour la Bottom Navigation Bar
class NavItem {
  final IconData icon;
  final IconData activeIcon;
  final String label;
  final int index;

  const NavItem({
    required this.icon,
    required this.activeIcon,
    required this.label,
    required this.index,
  });
}

/// Bottom Navigation Bar moderne avec indicateurs animés
class CustomBottomNavBar extends StatelessWidget {
  final int currentIndex;
  final ValueChanged<int> onTap;
  final List<NavItem> items;

  const CustomBottomNavBar({
    super.key,
    required this.currentIndex,
    required this.onTap,
    required this.items,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.1),
            blurRadius: 10,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: SafeArea(
        top: false,
        minimum: EdgeInsets.zero,
        child: Container(
          height: 52,
          padding: const EdgeInsets.symmetric(vertical: 2),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: items.map((item) {
              final isActive = currentIndex == item.index;
              return _NavItemWidget(
                item: item,
                isActive: isActive,
                onTap: () {
                  HapticFeedback.selectionClick();
                  onTap(item.index);
                },
              );
            }).toList(),
          ),
        ),
      ),
    );
  }
}

/// Widget pour un item de navigation
class _NavItemWidget extends StatelessWidget {
  final NavItem item;
  final bool isActive;
  final VoidCallback onTap;

  const _NavItemWidget({
    required this.item,
    required this.isActive,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: onTap,
          child: Container(
            padding: const EdgeInsets.symmetric(vertical: 2),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                SizedBox(
                  height: 22,
                  child: Stack(
                    alignment: Alignment.center,
                    clipBehavior: Clip.none,
                    children: [
                      // Indicateur actif
                      if (isActive)
                        Positioned(
                          bottom: -1,
                          child: Container(
                            width: 32,
                            height: 2,
                            decoration: BoxDecoration(
                              color: EcoColors.primaryGreen,
                              borderRadius: BorderRadius.circular(1),
                            ),
                          ),
                        ),
                      // Icône
                      Icon(
                        isActive ? item.activeIcon : item.icon,
                        size: isActive ? 22 : 20,
                        color: isActive
                            ? EcoColors.primaryGreen
                            : Colors.grey[600],
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 1),
                Text(
                  item.label,
                  style: TextStyle(
                    color: isActive
                        ? EcoColors.primaryGreen
                        : Colors.grey[600],
                    fontWeight: isActive ? FontWeight.bold : FontWeight.normal,
                    fontSize: 9,
                  ),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

