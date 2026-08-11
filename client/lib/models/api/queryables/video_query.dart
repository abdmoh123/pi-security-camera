import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class VideoQuery implements JsonSerialisable, HttpQueryable {
  final List<int>? videoIDs;
  final String? fileName;
  final List<int>? cameraIDs;
  final DateTime? uploadedAt;

  const VideoQuery({
    this.videoIDs,
    this.fileName,
    this.cameraIDs,
    this.uploadedAt,
  });

  @override
  String toHttpQueryString() {
    String query = "";
    if (videoIDs != null) {
      for (var i in videoIDs!) {
        query += "video_id=$i&";
      }
    }
    if (fileName != null) query += "&file_name=$fileName";
    if (cameraIDs != null) {
      for (var i in cameraIDs!) {
        query += "camera_id=$i&";
      }
    }
    if (uploadedAt != null) query += "&uploaded_at=$uploadedAt";
    return query;
  }

  @override
  Map<String, dynamic> toJson() => {
    if (videoIDs != null) 'video_ids': videoIDs,
    if (fileName != null) 'file_name': fileName,
    if (cameraIDs != null) 'camera_ids': cameraIDs,
    if (uploadedAt != null) 'uploaded_at': uploadedAt,
  };
}
