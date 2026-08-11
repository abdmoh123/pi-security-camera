import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class UserQuery implements JsonSerialisable, HttpQueryable {
  final int? id;
  final String? email;

  const UserQuery({this.id, this.email});

  @override
  String toHttpQueryString() {
    String query = "";
    if (id != null) query += "id=$id";
    if (email != null) query += "&email=$email";
    return query;
  }

  @override
  Map<String, dynamic> toJson() => {
    if (id != null) 'id': id,
    if (email != null) 'email': email,
  };
}
