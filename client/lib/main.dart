import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/date_symbol_data_local.dart';
import 'package:pisec_client/factories/downloader_factory.dart';
import 'package:pisec_client/models/api/queryables/user_query.dart';
import 'package:pisec_client/repositories/api/http/http_camera_repository.dart';
import 'package:pisec_client/repositories/api/http/http_video_repository.dart';
import 'package:pisec_client/repositories/token_repository.dart';
import 'package:pisec_client/screens/cameras.dart';
import 'package:pisec_client/screens/settings.dart';
import 'package:pisec_client/screens/videos.dart';
import 'package:pisec_client/services/auth_http_client.dart';
import 'package:pisec_client/services/login_api_service.dart';
import 'package:pisec_client/services/task_id_generators.dart';

void main() {
  const String baseUrl = "http://localhost:8000/api/v0";
  final tokenStorage = TokenRepository();
  final authService = LoginAPIService(baseUrl, http.Client());

  final client = AuthHttpClient(tokenStorage, authService);
  const user = UserQuery(
    email: "abdhawisa@gmail.com",
    password: "Emmajayne2020!",
  );
  // Logs the given user in
  client.init(user);

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
    Settings(),
  ];

  // Required to display the date in the correct format
  initializeDateFormatting("en_GB");
  runApp(PisecApp(pages: pages));
}

class PisecApp extends StatelessWidget {
  const PisecApp({super.key, required this.pages});

  final List<Widget> pages;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Pisec',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: MyHomePage(title: 'Pisec Home', pages: pages),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title, required this.pages});

  final String title;
  final List<Widget> pages;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int pageIndex = 0;

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
            label: "Camera",
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
