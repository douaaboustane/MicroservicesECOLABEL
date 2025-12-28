import 'package:equatable/equatable.dart';

/// Entité représentant un utilisateur
class User extends Equatable {
  final String id;
  final String email;
  final String? name;
  final String? pays;
  final String? token;

  const User({
    required this.id,
    required this.email,
    this.name,
    this.pays,
    this.token,
  });

  @override
  List<Object?> get props => [id, email, name, pays, token];
}
