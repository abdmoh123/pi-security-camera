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
  Map<String, dynamic> toJson() {
    return {'id': id, 'email': email, 'isAdmin': isAdmin};
  }
}
