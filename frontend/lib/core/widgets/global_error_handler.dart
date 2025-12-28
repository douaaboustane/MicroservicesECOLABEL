import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../constants/colors.dart';

/// Provider pour gérer les erreurs globales
final globalErrorProvider = StateNotifierProvider<GlobalErrorNotifier, String?>((ref) {
  return GlobalErrorNotifier();
});

class GlobalErrorNotifier extends StateNotifier<String?> {
  GlobalErrorNotifier() : super(null);

  void showError(String message) {
    state = message;
    // Auto-hide après 5 secondes
    Future.delayed(const Duration(seconds: 5), () {
      if (state == message) {
        state = null;
      }
    });
  }

  void clear() {
    state = null;
  }
}

/// Widget pour afficher les erreurs globales
class GlobalErrorBanner extends ConsumerWidget {
  const GlobalErrorBanner({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final error = ref.watch(globalErrorProvider);

    if (error == null) {
      return const SizedBox.shrink();
    }

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      color: EcoColors.error,
      child: Row(
        children: [
          const Icon(
            Icons.error_outline,
            color: Colors.white,
            size: 20,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              error,
              style: const TextStyle(
                color: Colors.white,
                fontSize: 12,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.close, color: Colors.white, size: 20),
            onPressed: () {
              ref.read(globalErrorProvider.notifier).clear();
            },
          ),
        ],
      ),
    );
  }
}


