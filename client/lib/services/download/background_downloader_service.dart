import 'package:background_downloader/background_downloader.dart';
import 'package:pisec_client/exceptions/download_exceptions.dart';
import 'package:pisec_client/models/event_task.dart';
import 'package:pisec_client/services/download/downloader_service.dart';

class BackgroundDownloaderService implements DownloaderService {
  // Used to generate unique task ids
  final String Function(String url) taskIdGenerator;

  const BackgroundDownloaderService(this.taskIdGenerator);

  @override
  Future<bool> cancelDownload(EventTask downloadTask) async {
    return await FileDownloader().cancelTaskWithId(downloadTask.id);
  }

  @override
  Future<EventTask?> downloadItem(String url, String fileName) async {
    // User picks where to save the file via native interface
    final Uri? directory = await FileDownloader().uri.pickDirectory();
    if (directory == null) {
      // Download cancelled by user
      return null;
    }

    final task = UriDownloadTask(
      taskId: taskIdGenerator(url),
      url: url,
      filename: fileName,
      directoryUri: directory,
    );

    final wasQueued = await FileDownloader().enqueue(task);
    if (!wasQueued) {
      throw DownloadException("Failed to enqueue task");
    }

    // Converts to generic task struct
    return EventTask(task.taskId);
  }
}
