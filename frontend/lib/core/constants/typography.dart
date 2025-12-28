import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// Typographie pour EcoLabel-MS
class EcoTypography {
  // Titres
  static TextStyle get h1 => GoogleFonts.poppins(
        fontSize: 32,
        fontWeight: FontWeight.bold,
        letterSpacing: -0.5,
      );

  static TextStyle get h2 => GoogleFonts.poppins(
        fontSize: 24,
        fontWeight: FontWeight.bold,
        letterSpacing: -0.3,
      );

  static TextStyle get h3 => GoogleFonts.poppins(
        fontSize: 20,
        fontWeight: FontWeight.w600,
        letterSpacing: -0.2,
      );

  static TextStyle get h4 => GoogleFonts.poppins(
        fontSize: 18,
        fontWeight: FontWeight.w600,
      );

  // Corps de texte
  static TextStyle get bodyLarge => GoogleFonts.inter(
        fontSize: 16,
        fontWeight: FontWeight.normal,
        height: 1.5,
      );

  static TextStyle get bodyMedium => GoogleFonts.inter(
        fontSize: 14,
        fontWeight: FontWeight.normal,
        height: 1.5,
      );

  static TextStyle get bodySmall => GoogleFonts.inter(
        fontSize: 12,
        fontWeight: FontWeight.normal,
        height: 1.4,
      );

  // Chiffres (scores)
  static TextStyle get scoreNumber => GoogleFonts.inter(
        fontSize: 48,
        fontWeight: FontWeight.w600,
        letterSpacing: -1,
      );

  static TextStyle get scoreLetter => GoogleFonts.poppins(
        fontSize: 72,
        fontWeight: FontWeight.bold,
        letterSpacing: -2,
      );

  // Labels & Captions
  static TextStyle get label => GoogleFonts.inter(
        fontSize: 12,
        fontWeight: FontWeight.w500,
        letterSpacing: 0.5,
      );

  static TextStyle get caption => GoogleFonts.inter(
        fontSize: 11,
        fontWeight: FontWeight.normal,
        color: Colors.grey[600],
      );
}
