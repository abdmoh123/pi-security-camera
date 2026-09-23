import 'package:flutter/material.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:pisec_client/factories/downloader_factory.dart';
import 'package:pisec_client/globals/notifier_provider.dart';
import 'package:pisec_client/repositories/api/http/http_camera_repository.dart';
import 'package:pisec_client/repositories/api/http/http_video_repository.dart';
import 'package:pisec_client/repositories/server_config_repository.dart';
import 'package:pisec_client/repositories/token_repository.dart';
import 'package:pisec_client/routes/route_args/login_route_args.dart';
import 'package:pisec_client/routes/route_generator.dart';
import 'package:pisec_client/screens/cameras_page.dart';
import 'package:pisec_client/screens/settings_page.dart';
import 'package:pisec_client/screens/videos_page.dart';
import 'package:pisec_client/services/auth_http_client.dart';
import 'package:pisec_client/services/login_api_service.dart';
import 'package:pisec_client/services/task_id_generators.dart';
import 'package:pisec_client/viewmodels/auth_state.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final serverConfig = ServerConfigRepository();
  String baseUrl = await serverConfig.getServerUrl();
  final tokenStorage = TokenRepository();
  final authService = LoginAPIService(baseUrl: baseUrl);

  final authState = AuthState(serverConfig, tokenStorage, authService);
  await authState.assertAuthenticated();
  final client = AuthHttpClient(
    tokenStorage,
    authService,
    onAuthGivenUp: authState.assertAuthenticated,
  );

  // Automatically chooses between web and native downloader
  final downloaderService = createDownloaderService(videoIdFromUrl);
  final videoRepository = HttpVideoRepository(
    client,
    baseUrl,
    downloaderService,
  );
  final cameraRepository = HttpCameraRepository(client, baseUrl);

  final List<Widget> pages = [
    VideosPage(videoRepository: videoRepository),
    CamerasPage(cameraRepository: cameraRepository),
    SettingsPage(),
  ];

  final routeGenerator = RouteGenerator(mainPages: pages, authState: authState);

  // Required to display the date in the correct format
  initializeDateFormatting("en_GB");
  runApp(PisecApp(routeGenerator: routeGenerator, authState: authState));
}

class PisecApp extends StatelessWidget {
  final RouteGenerator routeGenerator;
  final AuthState authState;

  const PisecApp({
    super.key,
    required this.routeGenerator,
    required this.authState,
  });

  @override
  Widget build(BuildContext context) {
    return NotifierProvider<AuthState>(
      notifier: authState,
      child: MaterialApp(
        title: 'Pisec',
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        ),
        onGenerateInitialRoutes: ((initialRoute) {
          if (!authState.isAuthenticated) {
            return [
              routeGenerator.generateRoutes(
                RouteSettings(
                  name: '/login',
                  arguments: LoginRouteArgs(serverUrl: authState.serverUrl),
                ),
              ),
            ];
          }
          return [routeGenerator.generateRoutes(RouteSettings(name: '/'))];
        }),
        onGenerateRoute: routeGenerator.generateRoutes,
      ),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({
    super.key,
    required this.title,
    required this.pages,
    this.initPageIndex = 0,
  });

  final String title;
  final List<Widget> pages;
  final int initPageIndex;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int pageIndex = 0;

  @override
  void initState() {
    super.initState();
    pageIndex = widget.initPageIndex;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(child: widget.pages[pageIndex]),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: pageIndex,
        items: [
          BottomNavigationBarItem(
            label: "Videos",
            activeIcon: Icon(Icons.camera_roll),
            icon: Icon(Icons.camera_roll_outlined),
          ),
          BottomNavigationBarItem(
            label: "Cameras",
            activeIcon: Icon(Icons.camera),
            icon: Icon(Icons.camera_outlined),
          ),
          BottomNavigationBarItem(
            label: "Settings",
            activeIcon: Icon(Icons.settings),
            icon: Icon(Icons.settings_outlined),
          ),
        ],
        onTap: _onTabTapped,
      ),
    );
  }

  void _onTabTapped(int index) {
    setState(() {
      pageIndex = index;
    });
  }
}
