import 'dart:io';

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:pisec_client/services/download/background_downloader_service.dart';
import 'package:pisec_client/services/download/browser_downloader_service.dart';
import 'package:pisec_client/services/download/desktop_downloader_service.dart';
import 'package:pisec_client/services/download/downloader_service.dart';

DownloaderService createDownloaderService(
  String Function(String url) taskIdGenerator,
) {
  if (kIsWeb) return BrowserDownloaderService();

  // For desktop OSes
  if (Platform.isLinux || Platform.isWindows || Platform.isMacOS) {
    return DesktopDownloaderService(taskIdGenerator);
  }
  // For android and probably iOS works too
  return BackgroundDownloaderService(taskIdGenerator);
}
