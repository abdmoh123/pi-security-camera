import 'package:pisec_client/models/const_datetime.dart';
import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class VideoQuery implements JsonSerialisable, PathQueryable {
  final List<int>? videoIDs;
  final String? fileName;
  final List<int>? cameraIDs;
  final ConstDateTime? uploadedAt;

  const VideoQuery({
    this.videoIDs,
    this.fileName,
    this.cameraIDs,
    this.uploadedAt,
  });

  @override
  String toPathQueryString() {
    String query = "";
    if (videoIDs != null) {
      for (var i in videoIDs!) {
        query += "&video_id=$i";
      }
    }
    if (fileName != null) query += "&file_name=$fileName";
    if (cameraIDs != null) {
      for (var i in cameraIDs!) {
        query += "&camera_id=$i";
      }
    }
    if (uploadedAt != null) query += "&uploaded_at=${uploadedAt!.toDateTime()}";
    return query == "" ? query : query.substring(1);
  }

  @override
  Map<String, dynamic> toJson() => {
    if (videoIDs != null) 'video_ids': videoIDs,
    if (fileName != null) 'file_name': fileName,
    if (cameraIDs != null) 'camera_ids': cameraIDs,
    if (uploadedAt != null) 'uploaded_at': uploadedAt!.toDateTime(),
  };
}
