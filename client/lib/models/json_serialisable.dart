abstract mixin class JsonSerialisable {
  Map<String, dynamic> toJson();

  static Map<String, String> createFakeJson(Iterable<String> keys) {
    return {for (var k in keys) k: '...'};
  }

  @override
  String toString() => toJson().toString();
}
