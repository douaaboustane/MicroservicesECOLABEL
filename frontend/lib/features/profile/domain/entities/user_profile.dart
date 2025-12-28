import 'package:equatable/equatable.dart';

/// Type d'alimentation
enum DietType {
  standard,
  vegetarian,
  vegan,
}

/// Objectifs écologiques
enum EcoGoal {
  reduceCo2,
  reduceWater,
  reduceEnergy,
}

/// Profil utilisateur
class UserProfile extends Equatable {
  final String id;
  final String? name;
  final String? avatarUrl;
  final String? country;
  final String? region;
  final DietType dietType;
  final List<EcoGoal> ecoGoals;
  final DateTime createdAt;
  final DateTime? updatedAt;

  const UserProfile({
    required this.id,
    this.name,
    this.avatarUrl,
    this.country,
    this.region,
    this.dietType = DietType.standard,
    this.ecoGoals = const [],
    required this.createdAt,
    this.updatedAt,
  });

  UserProfile copyWith({
    String? id,
    String? name,
    String? avatarUrl,
    String? country,
    String? region,
    DietType? dietType,
    List<EcoGoal>? ecoGoals,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return UserProfile(
      id: id ?? this.id,
      name: name ?? this.name,
      avatarUrl: avatarUrl ?? this.avatarUrl,
      country: country ?? this.country,
      region: region ?? this.region,
      dietType: dietType ?? this.dietType,
      ecoGoals: ecoGoals ?? this.ecoGoals,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? DateTime.now(),
    );
  }

  @override
  List<Object?> get props => [
        id,
        name,
        avatarUrl,
        country,
        region,
        dietType,
        ecoGoals,
        createdAt,
        updatedAt,
      ];
}
