import 'package:pisec_client/exceptions/download_exceptions.dart';

String videoIdFromUrl(String url) {
  final List<String> splitUrl = url.split("/");

  final int videoIndex = splitUrl.indexOf("videos");
  if (videoIndex == -1) {
    throw IdGenerationException("Failed to parse video id from url");
  }

  final videoId = int.tryParse(splitUrl[videoIndex + 1]);
  if (videoId == null) {
    throw IdGenerationException("Failed to parse video id from url");
  }

  return "pisec.videos.$videoId";
}
