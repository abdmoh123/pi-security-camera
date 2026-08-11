import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class User implements JsonSerialisable {
  final int id;
  final String email;
  final bool isAdmin;

  const User(this.id, this.email, {this.isAdmin = false});

  factory User.fromJson(Map<String, dynamic> json) {
    return User(json['id'], json['email'], isAdmin: json['isAdmin'] ?? false);
  }

  @override
  Map<String, dynamic> toJson() => {
    'id': id,
    'email': email,
    'is_admin': isAdmin,
  };

  static bool validateJson(Map<String, dynamic> json) {
    return json.containsKey('id') && json.containsKey('email');
  }

  static Map<String, dynamic> generateJsonStruct() {
    final keys = User(1, '').toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }
}

class UserQuery implements JsonSerialisable, HttpQueryable {
  final int? id;
  final String? email;

  const UserQuery({this.id, this.email});

  @override
  Map<String, dynamic> toJson() => {
    if (id != null) 'id': id,
    if (email != null) 'email': email,
  };

  @override
  String toHttpQueryString() {
    String query = "";
    if (id != null) query += "id=$id";
    if (email != null) query += "&email=$email";
    return query;
  }
}
