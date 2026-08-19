import 'package:flutter/material.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:pisec_client/models/api/responses/video_response.dart';
import 'package:pisec_client/screens/cameras.dart';
import 'package:pisec_client/screens/settings.dart';
import 'package:pisec_client/screens/videos.dart';

void main() {
  final List<VideoResponse> videos = [
    VideoResponse(1, "test1", 1, DateTime(0)),
    VideoResponse(2, "test2", 1, DateTime(1)),
    VideoResponse(3, "test3", 2, DateTime(0)),
  ];

  final List<Widget> pages = [Videos(videos: videos), Cameras(), Settings()];

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
      pageIndex = index;
    });
  }
}
