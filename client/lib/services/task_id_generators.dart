import 'package:pisec_client/exceptions/download_exceptions.dart';

String videoIdFromUrl(String url) {
  final splitUrl = url.split("/");
  int videoIndex = 0;
  for (var i = 0; i < splitUrl.length; i++) {
    if (splitUrl[i] == "videos") {
      break;
    }
    videoIndex++;
  }

  final videoId = int.tryParse(splitUrl[videoIndex + 1]);

  if (videoId == null) {
    throw IdGenerationException("Failed to parse video id from url");
  }
  return "pisec.videos.$videoId";
}
