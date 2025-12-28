import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/config/routes.dart';
import 'core/config/theme.dart';
import 'core/widgets/auth_guard.dart';
import 'core/widgets/network_banner.dart';
import 'core/widgets/global_error_handler.dart';
import 'core/widgets/main_scaffold.dart';
import 'features/auth/presentation/pages/login_page.dart';
import 'features/auth/presentation/pages/signup_page.dart';
import 'features/scan/presentation/pages/home_page.dart';
// Pages V2 activées avec design amélioré
import 'features/scan/presentation/pages/scan_page_v2.dart';
import 'features/scan/presentation/pages/preview_page_v2.dart';
import 'features/processing/presentation/pages/processing_page_v2.dart';
import 'features/result/presentation/pages/result_page.dart';
import 'features/history/presentation/pages/history_page.dart';
import 'features/settings/presentation/pages/settings_page.dart';
import 'features/result/presentation/pages/methodology_page.dart';
import 'features/auth/domain/usecases/login_usecase.dart';
import 'features/settings/domain/usecases/get_settings_usecase.dart';
import 'features/profile/domain/usecases/get_profile_usecase.dart';
import 'features/settings/presentation/pages/settings_page.dart';
import 'core/providers/theme_provider.dart';
import 'injection_container.dart' as di;

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialiser l'injection de dépendances AVANT de créer l'app
  await di.setupDependencyInjection();
  
  // Vérifier que les dépendances sont bien enregistrées
  assert(
    di.getIt.isRegistered<LoginUseCase>(),
    'LoginUseCase must be registered. Check setupDependencyInjection().',
  );
  assert(
    di.getIt.isRegistered<GetSettingsUseCase>(),
    'GetSettingsUseCase must be registered. Check setupDependencyInjection().',
  );
  assert(
    di.getIt.isRegistered<GetProfileUseCase>(),
    'GetProfileUseCase must be registered. Check setupDependencyInjection().',
  );
  
  runApp(
    const ProviderScope(
      child: EcoLabelApp(),
    ),
  );
}

class EcoLabelApp extends ConsumerWidget {
  const EcoLabelApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final themeMode = ref.watch(themeModeProvider);
    
    return MaterialApp(
      title: 'EcoLabel',
      theme: EcoTheme.lightTheme,
      darkTheme: EcoTheme.darkTheme,
      themeMode: themeMode,
      debugShowCheckedModeBanner: false,
      builder: (context, child) {
        // Ne pas envelopper dans un Scaffold si c'est MainScaffold
        // car MainScaffold a déjà son propre Scaffold avec Bottom Navigation
        final route = ModalRoute.of(context);
        final isMainScaffold = route?.settings.name == AppRoutes.home;
        
        if (isMainScaffold) {
          // Pour MainScaffold, ajouter les bannières directement dans le body
          return child ?? const SizedBox();
        }
        
        // Pour les autres pages, utiliser un Scaffold avec bannières
        return Scaffold(
          body: Column(
            children: [
              // Network banner en haut
              const NetworkBanner(),
              // Global error banner
              const GlobalErrorBanner(),
              // Contenu de l'app
              Expanded(child: child ?? const SizedBox()),
            ],
          ),
        );
      },
      initialRoute: AppRoutes.login,
      routes: {
        // Routes publiques
        AppRoutes.login: (context) => const LoginPage(),
        AppRoutes.signup: (context) => const SignupPage(),
        // Route principale avec Bottom Navigation
        AppRoutes.home: (context) => const AuthGuard(
              child: MainScaffold(),
            ),
        // Routes protégées (sans bottom nav) - Pages V2 activées
        AppRoutes.scan: (context) => const AuthGuard(
              child: ScanPageV2(),
            ),
        AppRoutes.preview: (context) {
          final args = ModalRoute.of(context)!.settings.arguments;
          return AuthGuard(
            child: PreviewPageV2(imageFile: args as dynamic),
          );
        },
        AppRoutes.processing: (context) {
          final jobId = ModalRoute.of(context)!.settings.arguments as String;
          return AuthGuard(
            child: ProcessingPageV2(jobId: jobId),
          );
        },
        AppRoutes.result: (context) {
          final jobId = ModalRoute.of(context)!.settings.arguments as String;
          return AuthGuard(
            child: ResultPage(jobId: jobId),
          );
        },
        AppRoutes.settings: (context) => const AuthGuard(
              child: SettingsPage(),
            ),
        AppRoutes.methodology: (context) => const AuthGuard(
              child: MethodologyPage(),
            ),
      },
    );
  }
}
