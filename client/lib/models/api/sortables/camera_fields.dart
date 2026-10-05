import 'package:pisec_client/types/sortable_field.dart';

enum CameraFields implements SortableField {
  camera,
  name,
  macAddress,
  date;

  @override
  String get fieldName {
    switch (this) {
      case CameraFields.camera:
        return "id";
      case CameraFields.name:
        return "name";
      case CameraFields.macAddress:
        return "mac_address";
      case CameraFields.date:
        return "registered_at";
    }
  }
}
