import 'dart:io';
import 'package:flutter/material.dart';
import '../../../../core/constants/colors.dart';
import '../../../../core/constants/strings.dart';
import '../../../../core/widgets/eco_button.dart';

/// Page de prévisualisation avant analyse
class PreviewPage extends StatelessWidget {
  final File imageFile;

  const PreviewPage({
    super.key,
    required this.imageFile,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: EcoColors.naturalBeige,
      appBar: AppBar(
        title: const Text(EcoStrings.previewTitle),
      ),
      body: Column(
        children: [
          Expanded(
            child: Image.file(
              imageFile,
              fit: BoxFit.contain,
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(24),
            child: EcoButton(
              text: EcoStrings.analyzeButton,
              icon: Icons.analytics,
              onPressed: () {
                // TODO: Lancer l'analyse
                Navigator.pop(context, imageFile);
              },
            ),
          ),
        ],
      ),
    );
  }
}
