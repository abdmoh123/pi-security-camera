import 'package:flutter/material.dart';
import 'package:pisec_client/models/api/responses/video_response.dart';
import 'package:pisec_client/widgets/video_card.dart';

class Videos extends StatelessWidget {
  final List<VideoResponse> videos;

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
        Expanded(
          child: ListView.builder(
            itemCount: videos.length,
            itemBuilder: (context, index) {
              return VideoCard(video: videos[index]);
            },
          ),
        ),
      ],
    );
  }
}
