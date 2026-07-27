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
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'fileName': fileName,
      'cameraID': cameraID,
      'uploadedAt': uploadedAt,
    };
  }
}
