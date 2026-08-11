import 'package:pisec_client/models/json_serialisable.dart';

class Camera implements JsonSerialisable {
  final int id;
  final String name;
  final String macAddress;

  const Camera(this.id, this.name, this.macAddress);

  factory Camera.fromJson(Map<String, dynamic> json) {
    return Camera(json['id'], json['name'], json['macAddress']);
  }

  @override
  Map<String, dynamic> toJson() => {
    'id': id,
    'name': name,
    'mac_address': macAddress,
  };

  static Map<String, dynamic> generateJsonStruct() {
    final keys = Camera(1, '', '').toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }

  static bool validateJson(Map<String, dynamic> json) {
    return json.containsKey('id') &&
        json.containsKey('name') &&
        json.containsKey('macAddress');
  }
}
