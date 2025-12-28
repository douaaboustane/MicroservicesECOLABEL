import '../../domain/entities/user_profile.dart';

/// Modèle de données pour UserProfile
class UserProfileModel extends UserProfile {
  const UserProfileModel({
    required super.id,
    super.name,
    super.avatarUrl,
    super.country,
    super.region,
    super.dietType,
    super.ecoGoals,
    required super.createdAt,
    super.updatedAt,
  });

  factory UserProfileModel.fromJson(Map<String, dynamic> json) {
    return UserProfileModel(
      id: json['id'] as String,
      name: json['name'] as String?,
      avatarUrl: json['avatar_url'] as String?,
      country: json['country'] as String?,
      region: json['region'] as String?,
      dietType: DietType.values.firstWhere(
        (e) => e.name == json['diet_type'],
        orElse: () => DietType.standard,
      ),
      ecoGoals: (json['eco_goals'] as List<dynamic>?)
              ?.map((e) => EcoGoal.values.firstWhere(
                    (goal) => goal.name == e,
                    orElse: () => EcoGoal.reduceCo2,
                  ))
              .toList() ??
          [],
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: json['updated_at'] != null
          ? DateTime.parse(json['updated_at'] as String)
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'avatar_url': avatarUrl,
      'country': country,
      'region': region,
      'diet_type': dietType.name,
      'eco_goals': ecoGoals.map((e) => e.name).toList(),
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
    };
  }
}
