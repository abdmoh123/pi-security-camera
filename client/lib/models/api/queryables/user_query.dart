import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class UserQuery implements JsonSerialisable, HttpQueryable {
  final List<int>? ids;
  final String? email;

  const UserQuery({this.ids, this.email});

  @override
  String toHttpQueryString() {
    String query = "";
    if (ids != null) {
      for (var i in ids!) {
        query += "id=$i&";
      }
    }
    if (email != null) query += "&email=$email";
    return query;
  }

  @override
  Map<String, dynamic> toJson() => {
    if (ids != null) 'id': ids,
    if (email != null) 'email': email,
  };
}
