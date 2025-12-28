import 'package:flutter/material.dart';
import 'dart:io';

/// Widget réutilisable pour les boutons de connexion sociale
class SocialLoginButtons extends StatelessWidget {
  final VoidCallback? onGooglePressed;
  final VoidCallback? onApplePressed;
  final VoidCallback? onMicrosoftPressed;
  final bool isLoading;

  const SocialLoginButtons({
    super.key,
    this.onGooglePressed,
    this.onApplePressed,
    this.onMicrosoftPressed,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        _SocialLoginButton(
          onPressed: isLoading ? null : onGooglePressed,
          borderColor: const Color(0xFF4285F4).withValues(alpha: 0.3),
          child: Image.asset(
            'assets/images/google_logo.png',
            width: 24,
            height: 24,
            errorBuilder: (context, error, stackTrace) {
              // Fallback si l'image n'existe pas
              return const Icon(Icons.g_mobiledata, size: 24, color: Color(0xFF4285F4));
            },
          ),
        ),
        if (Platform.isIOS || Platform.isMacOS) ...[
          const SizedBox(width: 16),
          _SocialLoginButton(
            onPressed: isLoading ? null : onApplePressed,
            borderColor: Colors.black.withValues(alpha: 0.3),
            child: Image.asset(
              'assets/images/apple_logo.png',
              width: 24,
              height: 24,
              errorBuilder: (context, error, stackTrace) {
                // Fallback si l'image n'existe pas
                return const Icon(Icons.apple, size: 24, color: Colors.black);
              },
            ),
          ),
        ],
        const SizedBox(width: 16),
        _SocialLoginButton(
          onPressed: isLoading ? null : onMicrosoftPressed,
          borderColor: const Color(0xFF00A4EF).withValues(alpha: 0.3),
          child: Image.asset(
            'assets/images/microsoft_logo.png',
            width: 24,
            height: 24,
            errorBuilder: (context, error, stackTrace) {
              // Fallback si l'image n'existe pas
              return const Icon(Icons.window, size: 24, color: Color(0xFF00A4EF));
            },
          ),
        ),
      ],
    );
  }
}

class _SocialLoginButton extends StatelessWidget {
  final VoidCallback? onPressed;
  final Widget child;
  final Color borderColor;

  const _SocialLoginButton({
    required this.onPressed,
    required this.child,
    required this.borderColor,
  });

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        onTap: onPressed,
        borderRadius: BorderRadius.circular(8),
        child: Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(8),
            border: Border.all(
              color: borderColor,
              width: 1.5,
            ),
          ),
          child: Center(child: child),
        ),
      ),
    );
  }
}


