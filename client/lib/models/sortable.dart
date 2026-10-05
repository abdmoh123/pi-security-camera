import 'package:pisec_client/types/sort_direction.dart';
import 'package:pisec_client/types/sortable_field.dart';

class Sortable<T extends SortableField> {
  final SortDirection direction;
  final T field;

  const Sortable({required this.direction, required this.field});

  @override
  String toString() => "${field.fieldName}:${direction.queryString}";
}
