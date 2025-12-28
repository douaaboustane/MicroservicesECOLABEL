import 'package:equatable/equatable.dart';

/// Requête d'inscription
class SignupRequest extends Equatable {
  final String email;
  final String password;
  final String? name;
  final String? pays;

  const SignupRequest({
    required this.email,
    required this.password,
    this.name,
    this.pays,
  });

  Map<String, dynamic> toJson() {
    return {
      'email': email,
      'password': password,
      if (name != null) 'name': name,
      if (pays != null) 'pays': pays,
    };
  }

  @override
  List<Object?> get props => [email, password, name, pays];
}
