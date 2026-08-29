import 'package:pisec_client/models/const_datetime.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class VideoResponse with JsonSerialisable {
  final int id;
  final String fileName;
  final int cameraID;
  final ConstDateTime uploadedAt;

  const VideoResponse(this.id, this.fileName, this.cameraID, this.uploadedAt);

  factory VideoResponse.fromJson(Map<String, dynamic> json) {
    return VideoResponse(
      json['id'],
      json['file_name'],
      json['camera_id'],
      ConstDateTime.fromDateTime(
        DateTime.parse(json['uploaded_at'] + "Z" as String).toLocal(),
      ),
    );
  }

  @override
  Map<String, dynamic> toJson() => {
    'id': id,
    'file_name': fileName,
    'camera_id': cameraID,
    'uploaded_at': uploadedAt.toDateTime(),
  };

  static Map<String, dynamic> generateJsonStruct() {
    final keys = VideoResponse(1, '', 1, ConstDateTime(0)).toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }

  static bool validateJson(Map<String, dynamic> json) {
    return json.containsKey('id') &&
        json.containsKey('file_name') &&
        json.containsKey('camera_id') &&
        json.containsKey('uploaded_at');
  }
}
