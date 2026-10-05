import 'package:pisec_client/types/sortable_field.dart';

enum VideoFields implements SortableField {
  video,
  cameraID,
  name,
  date;

  @override
  String get fieldName {
    switch (this) {
      case VideoFields.video:
        return "id";
      case VideoFields.cameraID:
        return "camera_id";
      case VideoFields.name:
        return "file_name";
      case VideoFields.date:
        return "uploaded_at";
    }
  }
}
