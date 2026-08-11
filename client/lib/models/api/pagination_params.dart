import 'package:pisec_client/models/json_serialisable.dart';

class PaginationParams implements JsonSerialisable {
  final int pageIndex;
  final int pageSize;

  const PaginationParams({this.pageIndex = 0, this.pageSize = 100});

  @override
  Map<String, dynamic> toJson() => {
    'page_index': pageIndex,
    'page_size': pageSize,
  };
}
