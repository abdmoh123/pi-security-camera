import 'package:pisec_client/models/event_task.dart';

abstract interface class DownloaderService {
  Future<bool> cancelDownload(EventTask downloadTask);

  Future<EventTask?> downloadItem(String url, String fileName);
}
