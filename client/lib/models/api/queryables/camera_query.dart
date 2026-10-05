import 'package:pisec_client/extensions/list.dart';
import 'package:pisec_client/models/api/sortables/camera_fields.dart';
import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/json_serialisable.dart';
import 'package:pisec_client/models/sortable.dart';

class CameraQuery implements JsonSerialisable, PathQueryable {
  final List<int>? cameraIDs;
  final String? name;
  final String? macAddress;
  final Sortable<CameraFields>? orderBy;

  const CameraQuery({this.cameraIDs, this.name, this.macAddress, this.orderBy});

  @override
  int genHashCode() => Object.hash(cameraIDs, name, macAddress, orderBy);

  @override
  bool isEqual(JsonSerialisable other) {
    if (other is! CameraQuery) return false;

    if (!cameraIDs.nullabilityEquals(other.cameraIDs)) return false;
    if (cameraIDs != null && cameraIDs!.length != other.cameraIDs!.length) {
      return false;
    }
    if (cameraIDs != null && !cameraIDs!.deepEquals(other.cameraIDs!)) {
      return false;
    }

    return name == other.name &&
        macAddress == other.macAddress &&
        orderBy.toString() == other.orderBy.toString();
  }

  @override
  Map<String, dynamic> toJson() => {
    if (cameraIDs != null) 'camera_ids': cameraIDs,
    if (name != null) 'name': name,
    if (macAddress != null) 'mac_address': macAddress,
    if (orderBy != null) 'order_by': orderBy!.toString(),
  };

  @override
  String toPathQueryString() {
    String query = "";
    if (cameraIDs != null) {
      for (var i in cameraIDs!) {
        query += "&camera_id=$i";
      }
    }
    if (name != null) query += "&name=$name";
    if (macAddress != null) query += "&mac_address=$macAddress";
    if (orderBy != null) query += "&order_by=${orderBy!.toString()}";
    return query == "" ? query : query.substring(1);
  }
}
