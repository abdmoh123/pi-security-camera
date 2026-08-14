import 'package:pisec_client/models/event_task.dart';
import 'package:pisec_client/services/download/downloader_service.dart';
import 'package:pisec_client/web/downloader.dart';

class BrowserDownloaderService implements DownloaderService {
  @override
  Future<bool> cancelDownload(EventTask downloadTask) async {
    // Delegate the cancelling to the browser as we can't do it
    return false;
  }

  @override
  Future<EventTask?> downloadItem(String url, String fileName) async {
    startDownload(url, fileName);

    // Returns a fake dummy task as we can't really do anything
    return EventTask("");
  }
}
