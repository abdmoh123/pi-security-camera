import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:pisec_client/models/api/responses/video_response.dart';
import 'package:pisec_client/models/event_task.dart';

const String locale = "en_GB";

enum MenuAction { download, delete }

class VideoTile extends StatelessWidget {
  final VideoResponse video;
  final bool isUnread;
  final Future<EventTask?> Function() _downloadVideo;
  final Future<VideoResponse> Function() _deleteVideo;

  const VideoTile({
    super.key,
    required this.video,
    required Future<EventTask?> Function() downloadVideo,
    required Future<VideoResponse> Function() deleteVideo,
    this.isUnread = true,
  }) : _downloadVideo = downloadVideo,
       _deleteVideo = deleteVideo;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Container(
        padding: const EdgeInsets.all(12.0),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.primaryContainer,
          border: Border.all(
            color: Theme.of(context).colorScheme.inversePrimary,
          ),
          borderRadius: BorderRadius.circular(8.0),
        ),
        child: Icon(Icons.movie),
      ),
      title: Text(
        video.fileName,
        textAlign: TextAlign.left,
        maxLines: 1,
        overflow: TextOverflow.ellipsis,
      ),
      subtitle: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            "camera-${video.cameraID.toString()}",
            textAlign: TextAlign.left,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
          Text(
            "${DateFormat.Hm(locale).format(video.uploadedAt.toDateTime())} ${DateFormat.yMd(locale).format(video.uploadedAt.toDateTime())}",
            textAlign: TextAlign.left,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
      // I am aware that I turned this off even though there are 3 lines.
      // It looks better this way
      isThreeLine: false,
      trailing: PopupMenuButton<MenuAction>(
        onSelected: (value) {
          switch (value) {
            case MenuAction.download:
              _downloadVideo();
              break;
            case MenuAction.delete:
              _deleteVideo();
              break;
          }
        },
        itemBuilder: (context) => [
          PopupMenuItem(
            value: MenuAction.download,
            child: ListTile(
              leading: Icon(Icons.download),
              title: Text("Download"),
            ),
          ),
          PopupMenuItem(
            value: MenuAction.delete,
            child: ListTile(leading: Icon(Icons.delete), title: Text("Delete")),
          ),
        ],
      ),
    );
  }
}
