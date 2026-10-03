import 'package:flutter/material.dart';

abstract mixin class JsonSerialisable {
  Map<String, dynamic> toJson();

  @protected
  bool isEqual(JsonSerialisable other);

  @protected
  int genHashCode();

  static Map<String, String> createFakeJson(Iterable<String> keys) {
    return {for (var k in keys) k: '...'};
  }

  @override
  String toString() => toJson().toString();

  @override
  bool operator ==(Object other) =>
      identical(this, other) || other is JsonSerialisable && isEqual(other);

  @override
  int get hashCode => genHashCode();
}
