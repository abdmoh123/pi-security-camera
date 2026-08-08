import 'package:flutter/material.dart';
import 'package:pisec_client/models/video.dart';
import 'package:pisec_client/widgets/video_card.dart';

class Videos extends StatelessWidget {
  final List<Video> videos;

  const Videos({super.key, required this.videos});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Container(
          padding: EdgeInsetsGeometry.all(8.0),
          child: Text("Videos", textAlign: TextAlign.center),
        ),
        ListView(children: videos.map((v) => VideoCard(video: v)).toList()),
      ],
    );
  }
}
