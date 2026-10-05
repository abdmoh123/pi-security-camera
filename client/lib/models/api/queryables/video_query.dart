import 'package:pisec_client/extensions/list.dart';
import 'package:pisec_client/models/api/sortables/video_fields.dart';
import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/json_serialisable.dart';
import 'package:pisec_client/models/sortable.dart';

class VideoQuery implements JsonSerialisable, PathQueryable {
  final List<int>? videoIDs;
  final String? fileName;
  final List<int>? cameraIDs;
  final Sortable<VideoFields>? orderBy;

  const VideoQuery({
    this.videoIDs,
    this.fileName,
    this.cameraIDs,
    this.orderBy,
  });

  @override
  int genHashCode() => Object.hash(videoIDs, fileName, cameraIDs, orderBy);

  @override
  bool isEqual(JsonSerialisable other) {
    if (other is! VideoQuery) return false;

    if (!videoIDs.nullabilityEquals(other.videoIDs)) return false;
    if (videoIDs != null && videoIDs!.length != other.videoIDs!.length) {
      return false;
    }
    if (videoIDs != null && !videoIDs!.deepEquals(other.videoIDs!)) {
      return false;
    }

    if (!cameraIDs.nullabilityEquals(other.cameraIDs)) return false;
    if (cameraIDs != null && cameraIDs!.length != other.cameraIDs!.length) {
      return false;
    }
    if (cameraIDs != null && !cameraIDs!.deepEquals(other.cameraIDs!)) {
      return false;
    }

    return fileName == other.fileName &&
        orderBy.toString() == other.orderBy.toString();
  }

  @override
  Map<String, dynamic> toJson() => {
    if (videoIDs != null) 'video_ids': videoIDs,
    if (fileName != null) 'file_name': fileName,
    if (cameraIDs != null) 'camera_ids': cameraIDs,
    if (orderBy != null) 'order_by': orderBy!.toString(),
  };

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
    if (orderBy != null) query += "&order_by=${orderBy!.toString()}";
    return query == "" ? query : query.substring(1);
  }
}
