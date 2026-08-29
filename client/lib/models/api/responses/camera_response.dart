import 'package:pisec_client/models/json_serialisable.dart';

class CameraResponse with JsonSerialisable {
  final int id;
  final String name;
  final String macAddress;

  const CameraResponse(this.id, this.name, this.macAddress);

  factory CameraResponse.fromJson(Map<String, dynamic> json) {
    return CameraResponse(json['id'], json['name'], json['mac_address']);
  }

  @override
  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'mac_address': macAddress,
  };

  static Map<String, dynamic> generateJsonStruct() {
    final keys = CameraResponse(1, '', '').toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }

  static bool validateJson(Map<String, dynamic> json) {
    return json.containsKey('id') &&
        json.containsKey('name') &&
        json.containsKey('mac_address');
  }
}
