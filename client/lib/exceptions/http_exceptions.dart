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
