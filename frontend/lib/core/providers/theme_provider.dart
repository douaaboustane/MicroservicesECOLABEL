import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Provider pour gérer le thème (dark/light mode)
final themeModeProvider = StateProvider<ThemeMode>((ref) => ThemeMode.light);

