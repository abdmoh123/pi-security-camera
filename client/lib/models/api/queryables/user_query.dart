import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/json_serialisable.dart';

class UserQuery implements JsonSerialisable, HttpQueryable {
  final List<int>? userIDs;
  final String? email;

  const UserQuery({this.userIDs, this.email});

  @override
  String toHttpQueryString() {
    String query = "";
    if (userIDs != null) {
      for (var i in userIDs!) {
        query += "&user_id=$i";
      }
    }
    if (email != null) query += "&email=$email";
    return query == "" ? query : query.substring(1);
  }

  @override
  Map<String, dynamic> toJson() => {
    if (userIDs != null) 'user_ids': userIDs,
    if (email != null) 'email': email,
  };
}
