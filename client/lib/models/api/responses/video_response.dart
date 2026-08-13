import 'package:pisec_client/models/json_serialisable.dart';

class VideoResponse implements JsonSerialisable {
  final int id;
  final String fileName;
  final int cameraID;
  final DateTime uploadedAt;

  const VideoResponse(this.id, this.fileName, this.cameraID, this.uploadedAt);

  factory VideoResponse.fromJson(Map<String, dynamic> json) {
    return VideoResponse(
      json['id'],
      json['fileName'],
      json['cameraID'],
      DateTime.parse(json['uploadedAt'] + "Z" as String).toLocal(),
    );
  }

  @override
  Map<String, dynamic> toJson() => {
    'id': id,
    'file_name': fileName,
    'camera_id': cameraID,
    'uploaded_at': uploadedAt,
  };

  static Map<String, dynamic> generateJsonStruct() {
    final keys = VideoResponse(1, '', 1, DateTime(0)).toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }

  static bool validateJson(Map<String, dynamic> json) {
    return json.containsKey('id') &&
        json.containsKey('fileName') &&
        json.containsKey('cameraID') &&
        json.containsKey('uploadedAt');
  }
}
