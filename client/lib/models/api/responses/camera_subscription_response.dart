import 'package:pisec_client/models/json_serialisable.dart';

class CameraSubscriptionResponse with JsonSerialisable {
  final int userID;
  final int cameraID;

  const CameraSubscriptionResponse(this.userID, this.cameraID);

  factory CameraSubscriptionResponse.fromJson(Map<String, dynamic> json) {
    return CameraSubscriptionResponse(json['user_id'], json['camera_id']);
  }

  @override
  Map<String, dynamic> toJson() => {'user_id': userID, 'camera_id': cameraID};

  static Map<String, dynamic> generateJsonStruct() {
    final keys = CameraSubscriptionResponse(1, 1).toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }

  static bool validateJson(Map<String, dynamic> json) {
    return json.containsKey('user_id') && json.containsKey('camera_id');
  }
}
