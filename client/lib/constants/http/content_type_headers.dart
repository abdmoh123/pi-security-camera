import 'package:http/http.dart';
import 'package:pisec_client/models/http/content_type_header.dart';

final ContentTypeHeader xWwwFormUrlencodedHeader = ContentTypeHeader(
  MediaType("application", "x-www-form-urlencoded"),
);
