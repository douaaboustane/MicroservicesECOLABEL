import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../constants/colors.dart';
import '../widgets/network_banner.dart';
import '../widgets/global_error_handler.dart';
import '../../features/scan/presentation/pages/home_page_v2.dart';
import '../../features/history/presentation/pages/history_page_v2.dart';
import '../../features/analytics/presentation/pages/insights_page.dart';
import '../../features/profile/presentation/pages/profile_page_v2.dart';

final currentPageIndexProvider = StateProvider<int>((ref) => 0);

class MainScaffold extends ConsumerWidget {
  const MainScaffold({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final currentIndex = ref.watch(currentPageIndexProvider);

    return Scaffold(
      backgroundColor: EcoColors.naturalBeige,
      // extendBody est essentiel pour que la page passe DERRIÈRE la barre flottante
      extendBody: true, 
      body: Stack(
        children: [
          // 1. Le contenu de la page
          Column(
            children: [
              const NetworkBanner(),
              const GlobalErrorBanner(),
              Expanded(child: _getPage(currentIndex)),
            ],
          ),

          // 2. La barre de navigation flottante
          // On utilise Align au lieu de Positioned pour mieux gérer le SafeArea
          Align(
            alignment: Alignment.bottomCenter,
            child: _buildCustomFloatingNavBar(context, ref, currentIndex),
          ),
        ],
      ),
    );
  }

  Widget _buildCustomFloatingNavBar(BuildContext context, WidgetRef ref, int currentIndex) {
    return SafeArea(
      child: Container(
        margin: const EdgeInsets.fromLTRB(16, 0, 16, 12),
        height: 72,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Colors.white.withOpacity(0.95),
              Colors.white.withOpacity(0.90),
            ],
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
          ),
          borderRadius: BorderRadius.circular(36),
          border: Border.all(
            color: Colors.white.withOpacity(0.3),
            width: 1.5,
          ),
          boxShadow: [
            BoxShadow(
              color: EcoColors.primaryGreen.withOpacity(0.12),
              blurRadius: 24,
              offset: const Offset(0, 8),
              spreadRadius: 0,
            ),
            BoxShadow(
              color: Colors.black.withOpacity(0.08),
              blurRadius: 16,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: ClipRRect(
          borderRadius: BorderRadius.circular(36),
          child: BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [
                    Colors.white.withOpacity(0.2),
                    Colors.white.withOpacity(0.1),
                  ],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _buildNavItem(
                    context: context,
                    ref: ref,
                    index: 0,
                    currentIndex: currentIndex,
                    icon: Icons.qr_code_scanner_rounded,
                    label: 'Scanner',
                  ),
                  _buildNavItem(
                    context: context,
                    ref: ref,
                    index: 1,
                    currentIndex: currentIndex,
                    icon: Icons.history_rounded,
                    label: 'Historique',
                  ),
                  _buildNavItem(
                    context: context,
                    ref: ref,
                    index: 2,
                    currentIndex: currentIndex,
                    icon: Icons.insights_rounded,
                    label: 'Insights',
                  ),
                  _buildNavItem(
                    context: context,
                    ref: ref,
                    index: 3,
                    currentIndex: currentIndex,
                    icon: Icons.person_rounded,
                    label: 'Profil',
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildNavItem({
    required BuildContext context,
    required WidgetRef ref,
    required int index,
    required int currentIndex,
    required IconData icon,
    required String label,
  }) {
    final isSelected = index == currentIndex;
    final color = isSelected ? EcoColors.primaryGreen : Colors.grey[500];

    return GestureDetector(
      onTap: () {
        ref.read(currentPageIndexProvider.notifier).state = index;
      },
      behavior: HitTestBehavior.opaque,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 250),
        curve: Curves.easeInOut,
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 2),
        decoration: BoxDecoration(
          color: isSelected 
              ? EcoColors.primaryGreen.withOpacity(0.12)
              : Colors.transparent,
          borderRadius: BorderRadius.circular(20),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          mainAxisSize: MainAxisSize.min,
          children: [
            AnimatedContainer(
              duration: const Duration(milliseconds: 250),
              curve: Curves.easeInOut,
              padding: const EdgeInsets.all(5),
              decoration: BoxDecoration(
                color: isSelected 
                    ? EcoColors.primaryGreen.withOpacity(0.15)
                    : Colors.transparent,
                shape: BoxShape.circle,
              ),
              child: Icon(
                icon,
                color: color,
                size: isSelected ? 24 : 22,
              ),
            ),
            const SizedBox(height: 2),
            AnimatedDefaultTextStyle(
              duration: const Duration(milliseconds: 250),
              style: TextStyle(
                color: color,
                fontSize: isSelected ? 10.5 : 10,
                fontWeight: isSelected ? FontWeight.w700 : FontWeight.w500,
                letterSpacing: 0.2,
                height: 1.0,
              ),
              child: Text(label),
            ),
          ],
        ),
      ),
    );
  }

  Widget _getPage(int index) {
    switch (index) {
      case 0:
        return const HomePageV2();
      case 1:
        return const HistoryPageV2();
      case 2:
        return const InsightsPage();
      case 3:
        return const ProfilePageV2();
      default:
        return const HomePageV2();
    }
  }
}