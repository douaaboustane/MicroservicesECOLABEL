import 'package:flutter/material.dart';

/// Bouton "@" pour insérer le symbole @ dans le champ email
/// À utiliser comme suffixIcon dans TextFormField
class EmailAtButton extends StatelessWidget {
  final TextEditingController controller;

  const EmailAtButton({
    super.key,
    required this.controller,
  });

  @override
  Widget build(BuildContext context) {
    return IconButton(
      icon: const Icon(Icons.alternate_email_outlined),
      onPressed: () {
        final text = controller.text;
        final selection = controller.selection;
        
        // Insérer "@" à la position du curseur
        final newText = text.replaceRange(
          selection.start,
          selection.end,
          '@',
        );
        
        controller.value = TextEditingValue(
          text: newText,
          selection: TextSelection.collapsed(
            offset: selection.start + 1,
          ),
        );
      },
    );
  }
}


