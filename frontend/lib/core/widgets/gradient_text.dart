import 'package:flutter/material.dart';

/// Widget de texte avec dégradé de couleur
class GradientText extends StatelessWidget {
  final String text;
  final Gradient gradient;
  final TextStyle? style;
  final TextAlign? textAlign;
  final bool shimmer;

  const GradientText({
    super.key,
    required this.text,
    required this.gradient,
    this.style,
    this.textAlign,
    this.shimmer = false,
  });

  @override
  Widget build(BuildContext context) {
    return ShaderMask(
      shaderCallback: (bounds) => gradient.createShader(
        Rect.fromLTWH(0, 0, bounds.width, bounds.height),
      ),
      child: Text(
        text,
        style: (style ?? const TextStyle()).copyWith(
          color: Colors.white,
        ),
        textAlign: textAlign,
      ),
    );
  }
}

