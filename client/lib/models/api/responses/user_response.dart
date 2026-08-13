import 'package:pisec_client/models/json_serialisable.dart';

class UserResponse implements JsonSerialisable {
  final int id;
  final String email;
  final bool isAdmin;

  const UserResponse(this.id, this.email, {this.isAdmin = false});

  factory UserResponse.fromJson(Map<String, dynamic> json) {
    return UserResponse(
      json['id'],
      json['email'],
      isAdmin: json['is_admin'] ?? false,
    );
  }

  @override
  Map<String, dynamic> toJson() => {
    'id': id,
    'email': email,
    'is_admin': isAdmin,
  };

  static Map<String, dynamic> generateJsonStruct() {
    final keys = UserResponse(1, '').toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }

  static bool validateJson(Map<String, dynamic> json) {
    return json.containsKey('id') && json.containsKey('email');
  }
}
