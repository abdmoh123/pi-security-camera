import 'package:pisec_client/extensions/list.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class PaginatedResponse<T extends JsonSerialisable> with JsonSerialisable {
  final List<T> items;
  final int pageIndex;
  final int pageSize;
  final int totalItems;
  final int totalPages;

  const PaginatedResponse({
    required this.items,
    required this.pageIndex,
    required this.pageSize,
    required this.totalItems,
    required this.totalPages,
  });

  factory PaginatedResponse.empty() => PaginatedResponse(
    items: List<T>.empty(),
    pageIndex: 0,
    pageSize: 1,
    totalItems: 0,
    totalPages: 0,
  );

  factory PaginatedResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Map<String, dynamic>) fromJsonT,
  ) {
    return PaginatedResponse(
      items: (json['items'] as List<dynamic>)
          .map((item) => fromJsonT(item as Map<String, dynamic>))
          .toList(),
      pageIndex: json['page_index'],
      pageSize: json['page_size'],
      totalItems: json['total_items'],
      totalPages: json['total_pages'],
    );
  }

  @override
  int genHashCode() =>
      Object.hash(items.hashCode, pageIndex, pageSize, totalItems, totalPages);

  @override
  bool isEqual(JsonSerialisable other) {
    if (other is! PaginatedResponse<T>) return false;

    if (items.length != other.items.length) return false;
    if (!items.deepEquals(other.items)) return false;

    return pageIndex == other.pageIndex &&
        pageSize == other.pageSize &&
        totalItems == other.totalItems &&
        totalPages == other.totalPages;
  }

  @override
  Map<String, dynamic> toJson() => {
    'items': items.map((item) => item.toJson()),
    'page_index': pageIndex,
    'page_size': pageSize,
    'total_items': totalItems,
    'total_pages': totalPages,
  };

  static Map<String, dynamic> generateJsonStruct<T extends JsonSerialisable>() {
    final keys = PaginatedResponse(
      items: List<T>.empty(),
      pageIndex: 0,
      pageSize: 0,
      totalItems: 0,
      totalPages: 0,
    ).toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }

  static bool validateJson(
    Map<String, dynamic> json,
    bool Function(Map<String, dynamic>) validateJsonT,
  ) {
    return json.containsKey('items') &&
        json['items'].every(
          (item) => validateJsonT(item as Map<String, dynamic>),
        ) &&
        json.containsKey('page_index') &&
        json.containsKey('page_size') &&
        json.containsKey('total_items') &&
        json.containsKey('total_pages');
  }
}
