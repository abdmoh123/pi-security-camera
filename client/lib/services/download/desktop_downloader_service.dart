import 'package:background_downloader/background_downloader.dart';
import 'package:file_selector/file_selector.dart';
import 'package:path_provider/path_provider.dart';
import 'package:pisec_client/exceptions/download_exceptions.dart';
import 'package:pisec_client/models/event_task.dart';
import 'package:pisec_client/services/download/downloader_service.dart';
import 'package:path/path.dart' as path;

const _mp4Type = XTypeGroup(
  label: "MP4 video",
  extensions: ["mp4"],
  mimeTypes: ["video/mp4"],
);

class DesktopDownloaderService implements DownloaderService {
  // Used to generate unique task ids
  final String Function(String url) taskIdGenerator;

  DesktopDownloaderService(this.taskIdGenerator) {
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
    final downloadDir = await getDownloadsDirectory();

    final FileSaveLocation? saveLocation = await getSaveLocation(
      acceptedTypeGroups: [_mp4Type],
      initialDirectory: downloadDir?.path,
      suggestedName: fileName,
      canCreateDirectories: true,
    );
    if (saveLocation == null) {
      // Download cancelled by user
      return null;
    }

    final task = DownloadTask(
      taskId: taskIdGenerator(url),
      url: url,
      filename: path.basename(saveLocation.path),
      baseDirectory: BaseDirectory.root,
      directory: path.dirname(saveLocation.path),
    );

    final result = await FileDownloader().download(task);
    switch (result.status) {
      case TaskStatus.enqueued:
      case TaskStatus.notFound:
      case TaskStatus.waitingToRetry:
      case TaskStatus.running:
      case TaskStatus.complete:
      case TaskStatus.paused:
      case TaskStatus.canceled:
        break;
      case TaskStatus.failed:
        throw DownloadException("Failed to download file");
    }

    // Converts to generic task struct
    return EventTask(task.taskId);
  }
}
