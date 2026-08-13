import 'package:pisec_client/models/json_serialisable.dart';

class UserQuery implements JsonSerialisable {
  final String? email;
  final String? password;

  const UserQuery({this.email, this.password});

  @override
  Map<String, dynamic> toJson() => {
    if (email != null) 'email': email,
    if (password != null) 'password': password,
  };
}
