import 'package:flutter/material.dart';
import 'package:pisec_client/models/video.dart';
import 'package:pisec_client/screens/cameras.dart';
import 'package:pisec_client/screens/settings.dart';
import 'package:pisec_client/screens/videos.dart';

void main() {
  runApp(const PisecApp());
}

class PisecApp extends StatelessWidget {
  const PisecApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Pisec',
      theme: ThemeData(
        // This is the theme of your application.
        //
        // TRY THIS: Try running your application with "flutter run". You'll see
        // the application has a purple toolbar. Then, without quitting the app,
        // try changing the seedColor in the colorScheme below to Colors.green
        // and then invoke "hot reload" (save your changes or press the "hot
        // reload" button in a Flutter-supported IDE, or press "r" if you used
        // the command line to start the app).
        //
        // Notice that the counter didn't reset back to zero; the application
        // state is not lost during the reload. To reset the state, use hot
        // restart instead.
        //
        // This works for code too, not just values: Most code changes can be
        // tested with just a hot reload.
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const MyHomePage(title: 'Pisec Home'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

enum PageType { videos, cameras, settings }

class _MyHomePageState extends State<MyHomePage> {
  PageType pageType = PageType.videos;

  static Map<PageType, Widget> pages = {
    PageType.videos: Videos(videos: _videos),
    PageType.cameras: Cameras(),
    PageType.settings: Settings(),
  };

  static final _videos = [
    Video(1, "test1", 1, DateTime(0)),
    Video(2, "test2", 1, DateTime(1)),
    Video(3, "test3", 2, DateTime(0)),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(child: pages[pageType]),
      bottomNavigationBar: BottomNavigationBar(
        items: [
          BottomNavigationBarItem(
            label: "Videos",
            icon: Icon(Icons.camera_roll),
          ),
          BottomNavigationBarItem(label: "Camera", icon: Icon(Icons.camera)),
          BottomNavigationBarItem(
            label: "Settings",
            icon: Icon(Icons.settings),
          ),
        ],
        onTap: _onTabTapped,
      ),
    );
  }

  void _onTabTapped(int index) {
    setState(() {
      pageType = switch (index) {
        0 => PageType.videos,
        1 => PageType.cameras,
        2 => PageType.settings,
        _ => PageType.videos,
      };
    });
  }
}
