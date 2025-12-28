import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:get_it/get_it.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'core/network/api_client.dart';
import 'core/network/network_info.dart';
import 'features/auth/data/datasources/auth_remote_ds.dart';
import 'features/auth/data/datasources/auth_local_ds.dart';
import 'features/auth/data/repositories/auth_repository_impl.dart';
import 'features/auth/domain/repositories/auth_repository.dart';
import 'features/auth/domain/usecases/login_usecase.dart';
import 'features/auth/domain/usecases/signup_usecase.dart';
import 'features/auth/domain/usecases/logout_usecase.dart';
import 'features/auth/domain/usecases/get_current_user_usecase.dart';
import 'features/auth/domain/usecases/update_profile_usecase.dart' as auth_update;
import 'features/auth/domain/usecases/social_auth_usecase.dart';
import 'features/scan/data/datasources/scan_remote_ds.dart';
import 'features/scan/data/repositories/scan_repository_impl.dart';
import 'features/scan/domain/repositories/scan_repository.dart';
import 'features/scan/domain/usecases/create_scan_job.dart';
import 'features/processing/data/datasources/job_polling_ds.dart';
import 'features/processing/domain/usecases/track_job_status.dart';
import 'features/result/data/repositories/result_repository_impl.dart';
import 'features/result/domain/usecases/get_final_score.dart';
import 'features/profile/data/datasources/profile_local_ds.dart';
import 'features/profile/data/repositories/profile_repository_impl.dart';
import 'features/profile/domain/repositories/profile_repository.dart';
import 'features/profile/domain/usecases/get_profile_usecase.dart';
import 'features/profile/domain/usecases/update_profile_usecase.dart';
import 'features/settings/data/datasources/settings_local_ds.dart';
import 'features/settings/data/repositories/settings_repository_impl.dart';
import 'features/settings/domain/repositories/settings_repository.dart';
import 'features/settings/domain/usecases/get_settings_usecase.dart';
import 'features/settings/domain/usecases/update_settings_usecase.dart';
import 'features/analytics/data/datasources/analytics_remote_ds.dart';
import 'features/analytics/data/repositories/analytics_repository_impl.dart';
import 'features/analytics/domain/repositories/analytics_repository.dart';
import 'features/analytics/domain/usecases/get_trends_usecase.dart';
import 'features/analytics/domain/usecases/get_top_ingredients_usecase.dart';
import 'features/analytics/domain/usecases/get_bad_ingredients_usecase.dart';
import 'features/analytics/domain/usecases/get_recommendations_usecase.dart';
import 'features/analytics/domain/usecases/get_anomalies_usecase.dart';

/// Conteneur d'injection de dépendances
final getIt = GetIt.instance;

Future<void> setupDependencyInjection() async {
  // Core
  final sharedPreferences = await SharedPreferences.getInstance();
  getIt.registerLazySingleton(() => sharedPreferences);
  getIt.registerLazySingleton(() => ApiClient(getIt<SharedPreferences>()));
  getIt.registerLazySingleton(() => Connectivity());
  getIt.registerLazySingleton(() => NetworkInfo(getIt()));

  // Auth Feature
  getIt.registerLazySingleton<AuthRemoteDataSource>(
    () => AuthRemoteDataSource(getIt<ApiClient>()),
  );
  getIt.registerLazySingleton<AuthLocalDataSource>(
    () => AuthLocalDataSource(getIt<SharedPreferences>()),
  );
  getIt.registerLazySingleton<AuthRepository>(
    () => AuthRepositoryImpl(
      remoteDataSource: getIt<AuthRemoteDataSource>(),
      localDataSource: getIt<AuthLocalDataSource>(),
    ),
  );
  getIt.registerLazySingleton(() => LoginUseCase(getIt<AuthRepository>()));
  getIt.registerLazySingleton(() => SignupUseCase(getIt<AuthRepository>()));
  getIt.registerLazySingleton(() => LogoutUseCase(getIt<AuthRepository>()));
  getIt.registerLazySingleton(
    () => GetCurrentUserUseCase(getIt<AuthRepository>()),
  );
  getIt.registerLazySingleton(
    () => auth_update.UpdateProfileUseCase(getIt<AuthRepository>()),
  );
  getIt.registerLazySingleton(
    () => SocialAuthUseCase(getIt<AuthRepository>()),
  );

  // Scan Feature
  getIt.registerLazySingleton<ScanRemoteDataSource>(
    () => ScanRemoteDataSource(getIt<ApiClient>()),
  );
  getIt.registerLazySingleton<ScanRepository>(
    () => ScanRepositoryImpl(getIt<ScanRemoteDataSource>()),
  );
  getIt.registerLazySingleton(() => CreateScanJob(getIt<ScanRepository>()));

  // Processing Feature
  getIt.registerLazySingleton<JobPollingDataSource>(
    () => JobPollingDataSource(getIt<ApiClient>()),
  );
  getIt.registerLazySingleton(
    () => TrackJobStatus(getIt<JobPollingDataSource>()),
  );

  // Result Feature
  getIt.registerLazySingleton<ResultRepositoryImpl>(
    () => ResultRepositoryImpl(getIt<ApiClient>()),
  );
  getIt.registerLazySingleton(
    () => GetFinalScore(getIt<ResultRepositoryImpl>()),
  );

  // Profile Feature
  getIt.registerLazySingleton<ProfileLocalDataSource>(
    () => ProfileLocalDataSource(getIt<SharedPreferences>()),
  );
  getIt.registerLazySingleton<ProfileRepository>(
    () => ProfileRepositoryImpl(getIt<ProfileLocalDataSource>()),
  );
  getIt.registerLazySingleton(
    () => GetProfileUseCase(getIt<ProfileRepository>()),
  );
  getIt.registerLazySingleton(
    () => UpdateProfileUseCase(getIt<ProfileRepository>()),
  );

  // Settings Feature
  getIt.registerLazySingleton<SettingsLocalDataSource>(
    () => SettingsLocalDataSource(getIt<SharedPreferences>()),
  );
  getIt.registerLazySingleton<SettingsRepository>(
    () => SettingsRepositoryImpl(getIt<SettingsLocalDataSource>()),
  );
  getIt.registerLazySingleton(
    () => GetSettingsUseCase(getIt<SettingsRepository>()),
  );
  getIt.registerLazySingleton(
    () => UpdateSettingsUseCase(getIt<SettingsRepository>()),
  );

  // Analytics Feature
  getIt.registerLazySingleton<AnalyticsRemoteDataSource>(
    () => AnalyticsRemoteDataSource(getIt<ApiClient>()),
  );
  getIt.registerLazySingleton<AnalyticsRepository>(
    () => AnalyticsRepositoryImpl(getIt<AnalyticsRemoteDataSource>()),
  );
  getIt.registerLazySingleton(
    () => GetTrendsUseCase(getIt<AnalyticsRepository>()),
  );
  getIt.registerLazySingleton(
    () => GetTopIngredientsUseCase(getIt<AnalyticsRepository>()),
  );
  getIt.registerLazySingleton(
    () => GetBadIngredientsUseCase(getIt<AnalyticsRepository>()),
  );
  getIt.registerLazySingleton(
    () => GetRecommendationsUseCase(getIt<AnalyticsRepository>()),
  );
  getIt.registerLazySingleton(
    () => GetAnomaliesUseCase(getIt<AnalyticsRepository>()),
  );
}
