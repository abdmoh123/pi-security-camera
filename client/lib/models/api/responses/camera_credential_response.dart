import 'package:pisec_client/models/json_serialisable.dart';

class CameraCredentialResponse with JsonSerialisable {
  final String clientID;
  final int userID;
  final String clientSecret;

  const CameraCredentialResponse(this.clientID, this.userID, this.clientSecret);

  factory CameraCredentialResponse.fromJson(Map<String, dynamic> json) {
    return CameraCredentialResponse(
      json['client_id'],
      json['user_id'],
      json['client_secret'],
    );
  }

  @override
  Map<String, dynamic> toJson() => {
    'client_id': clientID,
    'user_id': userID,
    'client_secret': clientSecret,
  };

  static Map<String, dynamic> generateJsonStruct() {
    final keys = CameraCredentialResponse("", 1, "").toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }

  static bool validateJson(Map<String, dynamic> json) {
    return json.containsKey('client_id') &&
        json.containsKey('user_id') &&
        json.containsKey('client_secret');
  }
}
