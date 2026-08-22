import 'package:pisec_client/models/const_datetime.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class VideoUrlResponse implements JsonSerialisable {
  final String url;
  final ConstDateTime expiresAt;

  const VideoUrlResponse(this.url, this.expiresAt);

  factory VideoUrlResponse.fromJson(Map<String, dynamic> json) {
    return VideoUrlResponse(
      json['url'],
      ConstDateTime.fromDateTime(
        DateTime.parse(json['expires_at'] + "Z" as String).toLocal(),
      ),
    );
  }

  @override
  Map<String, dynamic> toJson() => {
    'url': url,
    'expires_at': expiresAt.toDateTime(),
  };

  static Map<String, dynamic> generateJsonStruct() {
    final keys = const VideoUrlResponse('', ConstDateTime(0)).toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }

  static bool validateJson(Map<String, dynamic> json) {
    return json.containsKey('url') && json.containsKey('expires_at');
  }
}
