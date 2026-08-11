import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class CameraQuery implements JsonSerialisable, HttpQueryable {
  final List<int>? ids;
  final String? name;
  final String? macAddress;

  const CameraQuery({this.ids, this.name, this.macAddress});

  @override
  String toHttpQueryString() {
    String query = "";
    if (ids != null) {
      for (var i in ids!) {
        query += "id=$i&";
      }
    }
    if (name != null) query += "&name=$name";
    if (macAddress != null) query += "&mac_address=$macAddress";
    return query;
  }

  @override
  Map<String, dynamic> toJson() => {
    if (ids != null) 'id': ids,
    if (name != null) 'name': name,
    if (macAddress != null) 'mac_address': macAddress,
  };
}
