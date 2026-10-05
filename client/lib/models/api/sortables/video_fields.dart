import 'package:pisec_client/types/sortable_field.dart';

enum VideoFields implements SortableField {
  date,
  cameraID;

  @override
  String get fieldName {
    switch (this) {
      case VideoFields.date:
        return "uploaded_at";
      case VideoFields.cameraID:
        return "camera_id";
    }
  }
}
