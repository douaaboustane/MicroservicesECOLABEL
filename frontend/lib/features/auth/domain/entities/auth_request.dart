import 'package:equatable/equatable.dart';

/// Requête d'authentification
class AuthRequest extends Equatable {
  final String email;
  final String password;

  const AuthRequest({
    required this.email,
    required this.password,
  });

  @override
  List<Object?> get props => [email, password];
}
