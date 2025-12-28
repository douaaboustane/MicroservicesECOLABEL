import '../../domain/entities/user.dart';

/// Modèle de données pour User
class UserModel extends User {
  const UserModel({
    required super.id,
    required super.email,
    super.name,
    super.pays,
    super.token,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      email: json['email'] as String,
      name: json['name'] as String?,
      pays: json['pays'] as String?,
      token: json['token'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      if (name != null) 'name': name,
      if (pays != null) 'pays': pays,
      if (token != null) 'token': token,
    };
  }
}
