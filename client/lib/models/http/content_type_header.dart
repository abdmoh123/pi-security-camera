import 'dart:io';

import 'package:http/http.dart';
import 'package:pisec_client/models/http/http_header.dart';

class ContentTypeHeader implements HttpHeader {
  final MediaType contentType;

  const ContentTypeHeader(this.contentType);

  @override
  Map<String, String> toDict() => {
    HttpHeaders.contentTypeHeader: contentType.mimeType,
  };
}
