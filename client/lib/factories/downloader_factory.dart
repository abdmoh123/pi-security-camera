import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:pisec_client/services/download/background_downloader_service.dart';
import 'package:pisec_client/services/download/browser_downloader_service.dart';
import 'package:pisec_client/services/download/downloader_service.dart';

DownloaderService createDownloaderService(
  String Function(String url) taskIdGenerator,
) {
  return kIsWeb
      ? BrowserDownloaderService()
      : BackgroundDownloaderService(taskIdGenerator);
}
