import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class VideoQuery implements JsonSerialisable, HttpQueryable {
  final int? id;
  final String? fileName;
  final int? cameraID;
  final DateTime? uploadedAt;

  const VideoQuery({this.id, this.fileName, this.cameraID, this.uploadedAt});

  @override
  String toHttpQueryString() {
    String query = "";
    if (id != null) query += "id=$id";
    if (fileName != null) query += "&file_name=$fileName";
    if (cameraID != null) query += "&camera_id=$cameraID";
    if (uploadedAt != null) query += "&uploaded_at=$uploadedAt";
    return query;
  }

  @override
  Map<String, dynamic> toJson() => {
    if (id != null) 'id': id,
    if (fileName != null) 'file_name': fileName,
    if (cameraID != null) 'camera_id': cameraID,
    if (uploadedAt != null) 'uploaded_at': uploadedAt,
  };
}
