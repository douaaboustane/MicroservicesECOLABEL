import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../domain/entities/user_profile.dart';
import '../domain/usecases/get_profile_usecase.dart';
import '../domain/usecases/update_profile_usecase.dart';

/// Controller pour le profil utilisateur
class ProfileController extends StateNotifier<AsyncValue<UserProfile?>> {
  final GetProfileUseCase getProfileUseCase;
  final UpdateProfileUseCase updateProfileUseCase;

  ProfileController({
    required this.getProfileUseCase,
    required this.updateProfileUseCase,
  }) : super(const AsyncValue.loading()) {
    _loadProfile();
  }

  Future<void> _loadProfile() async {
    try {
      final profile = await getProfileUseCase();
      state = AsyncValue.data(profile);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }

  Future<void> updateProfile(UserProfile profile) async {
    state = const AsyncValue.loading();
    try {
      final updated = await updateProfileUseCase(profile);
      state = AsyncValue.data(updated);
    } catch (e, stack) {
      state = AsyncValue.error(e, stack);
    }
  }
}
