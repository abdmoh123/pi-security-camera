import 'dart:io';

class HttpCodedException extends HttpException {
  final int statusCode;

  HttpCodedException({
    required this.statusCode,
    required String message,
    Uri? uri,
  }) : super(message, uri: uri);

  @override
  String toString() {
    return "Error $statusCode: ${super.toString()}";
  }
}

class ResponseMismatchException implements Exception {
  final Map<String, dynamic> expected;
  final Map<String, dynamic> actual;
  final String message;

  ResponseMismatchException(this.expected, this.actual, {this.message = ""});

  @override
  String toString() {
    if (message.isNotEmpty) {
      return message;
    }
    return "Expected: $expected\nActual: $actual";
  }
}
