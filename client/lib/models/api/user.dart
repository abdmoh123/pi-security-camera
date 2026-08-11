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
