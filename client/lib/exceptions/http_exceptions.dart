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

class JsonResponseMismatchException
    extends ResponseMismatchException<Map<String, dynamic>> {
  JsonResponseMismatchException(
    super.expected,
    super.actual, {
    super.message = "",
  });
}

class ResponseMismatchException<T> implements Exception {
  final T expected;
  final T actual;
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
