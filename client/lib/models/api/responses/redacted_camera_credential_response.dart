import 'package:pisec_client/models/const_datetime.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class RedactedCameraCredentialResponse with JsonSerialisable {
  final String clientID;
  final int userID;
  final int? cameraID;
  final ConstDateTime registeredAt;

  const RedactedCameraCredentialResponse(
    this.clientID,
    this.userID,
    this.registeredAt, {
    this.cameraID,
  });

  factory RedactedCameraCredentialResponse.fromJson(Map<String, dynamic> json) {
    return RedactedCameraCredentialResponse(
      json['client_id'],
      json['user_id'],
      ConstDateTime.fromDateTime(
        DateTime.parse(
          (json['registered_at'] as String).replaceAll(
            '"',
            '',
          ), // Remove quotes
        ).toLocal(),
      ),
      cameraID: json['camera_id'],
    );
  }

  @override
  Map<String, dynamic> toJson() => {
    'client_id': clientID,
    'user_id': userID,
    if (cameraID != null) 'camera_id': cameraID,
    'registered_at': registeredAt.toDateTime(),
  };

  static Map<String, dynamic> generateJsonStruct() {
    final keys = const RedactedCameraCredentialResponse(
      "",
      1,
      ConstDateTime(0),
    ).toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }

  static bool validateJson(Map<String, dynamic> json) {
    return json.containsKey('client_id') &&
        json.containsKey('user_id') &&
        json.containsKey('registered_at');
  }
}
