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

  return "pisec.videos.$videoId";
}
