import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class VideoQuery implements JsonSerialisable, HttpQueryable {
  final List<int>? ids;
  final String? fileName;
  final List<int>? cameraIDs;
  final DateTime? uploadedAt;

  const VideoQuery({this.ids, this.fileName, this.cameraIDs, this.uploadedAt});

  @override
  String toHttpQueryString() {
    String query = "";
    if (ids != null) {
      for (var i in ids!) {
        query += "id=$i&";
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
    if (ids != null) 'id': ids,
    if (fileName != null) 'file_name': fileName,
    if (cameraIDs != null) 'camera_id': cameraIDs,
    if (uploadedAt != null) 'uploaded_at': uploadedAt,
  };
}
