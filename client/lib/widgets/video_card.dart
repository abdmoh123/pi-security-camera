import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:pisec_client/models/video.dart';

const String locale = "en_GB";

enum MenuAction { delete }

class VideoCard extends StatelessWidget {
  final Video video;
  final bool isUnread;

  const VideoCard({super.key, required this.video, this.isUnread = true});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Container(
        padding: const EdgeInsets.all(8.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(video.fileName, textAlign: TextAlign.left),
                    Text(
                      "camera-${video.cameraID.toString()}",
                      textAlign: TextAlign.left,
                    ),
                  ],
                ),
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text(
                      DateFormat.Hm(locale).format(video.uploadedAt),
                      textAlign: TextAlign.right,
                    ),
                    Text(
                      DateFormat.yMd(locale).format(video.uploadedAt),
                      textAlign: TextAlign.right,
                    ),
                  ],
                ),
                PopupMenuButton<MenuAction>(
                  onSelected: (value) {
                    switch (value) {
                      case MenuAction.delete:
                        break;
                    }
                  },
                  itemBuilder: (context) => [
                    PopupMenuItem(
                      value: MenuAction.delete,
                      child: ListTile(
                        leading: Icon(Icons.delete),
                        title: Text("Delete"),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
