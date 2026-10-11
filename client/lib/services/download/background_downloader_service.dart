import 'package:background_downloader/background_downloader.dart';
import 'package:pisec_client/exceptions/download_exceptions.dart';
import 'package:pisec_client/models/event_task.dart';
import 'package:pisec_client/services/download/downloader_service.dart';

class BackgroundDownloaderService implements DownloaderService {
  // Used to generate unique task ids
  final String Function(String url) taskIdGenerator;

  BackgroundDownloaderService(this.taskIdGenerator) {
    FileDownloader().configure(
      globalConfig: [(Config.requestTimeout, const Duration(seconds: 100))],
      androidConfig: [(Config.useCacheDir, Config.whenAble)],
    );

    FileDownloader().configureNotificationForGroup(
      FileDownloader.defaultGroup,
      running: const TaskNotification(
        "Downloading {filename}",
        "Progress: {progress} - Time remaining: {timeRemaining}",
      ),
      complete: const TaskNotification(
        "Download complete",
        "Successfully downloaded {filename}",
      ),
      error: const TaskNotification(
        "Download error",
        "Failed to download {filename}",
      ),
      paused: const TaskNotification(
        "Download paused",
        "Download for {filename} was paused",
      ),
      canceled: const TaskNotification(
        "Download cancelled",
        "Download cancelled for {filename}",
      ),
      progressBar: true,
      tapOpensFile: true,
    );
  }

  @override
  Future<void> init() async {
    await FileDownloader().start(autoCleanDatabase: true);
    // TODO: Maybe support resuming downloads
  }

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
