class DownloadException implements Exception {
  final String message;

  const DownloadException(this.message);

  @override
  String toString() => message;
}

class IdGenerationException implements Exception {
  final String message;

  const IdGenerationException(this.message);

  @override
  String toString() => message;
}
