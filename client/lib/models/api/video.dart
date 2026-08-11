import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class Video implements JsonSerialisable {
  final int id;
  final String fileName;
  final int cameraID;
  final DateTime uploadedAt;

  const Video(this.id, this.fileName, this.cameraID, this.uploadedAt);

  factory Video.fromJson(Map<String, dynamic> json) {
    return Video(
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

  static bool validateJson(Map<String, dynamic> json) {
    return json.containsKey('id') &&
        json.containsKey('fileName') &&
        json.containsKey('cameraID') &&
        json.containsKey('uploadedAt');
  }

  static Map<String, dynamic> generateJsonStruct() {
    final keys = Video(1, '', 1, DateTime(0)).toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }
}

class VideoQuery implements JsonSerialisable, HttpQueryable {
  final int? id;
  final String? fileName;
  final int? cameraID;
  final DateTime? uploadedAt;

  const VideoQuery({this.id, this.fileName, this.cameraID, this.uploadedAt});

  @override
  Map<String, dynamic> toJson() => {
    if (id != null) 'id': id,
    if (fileName != null) 'file_name': fileName,
    if (cameraID != null) 'camera_id': cameraID,
    if (uploadedAt != null) 'uploaded_at': uploadedAt,
  };

  @override
  String toHttpQueryString() {
    String query = "";
    if (id != null) query += "id=$id";
    if (fileName != null) query += "&file_name=$fileName";
    if (cameraID != null) query += "&camera_id=$cameraID";
    if (uploadedAt != null) query += "&uploaded_at=$uploadedAt";
    return query;
  }
}
