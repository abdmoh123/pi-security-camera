import 'package:web/web.dart' as web;

void startDownload(String url, String fileName) {
  // Create an invisible anchor that is clicked to trigger a download
  final anchor = web.document.createElement('a') as web.HTMLAnchorElement
    ..href = url
    ..download = fileName
    ..style.display = 'none';

  web.document.body!.append(anchor);
  anchor.click();
  anchor.remove();
}
