import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class CameraQuery implements JsonSerialisable, HttpQueryable {
  final int? id;
  final String? name;
  final String? macAddress;

  const CameraQuery({this.id, this.name, this.macAddress});

  @override
  String toHttpQueryString() {
    String query = "";
    if (id != null) query += "id=$id";
    if (name != null) query += "&name=$name";
    if (macAddress != null) query += "&mac_address=$macAddress";
    return query;
  }

  @override
  Map<String, dynamic> toJson() => {
    if (id != null) 'id': id,
    if (name != null) 'name': name,
    if (macAddress != null) 'mac_address': macAddress,
  };
}
