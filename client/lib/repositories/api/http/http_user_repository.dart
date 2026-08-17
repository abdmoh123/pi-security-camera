import 'dart:convert';

import 'package:pisec_client/exceptions/http_exceptions.dart';
import 'package:pisec_client/extensions/http.dart';
import 'package:pisec_client/models/api/queryables/pagination_params.dart';
import 'package:pisec_client/models/api/queryables/user_query.dart';
import 'package:pisec_client/models/api/responses/camera_credential_response.dart';
import 'package:pisec_client/models/api/responses/user_response.dart';
import 'package:pisec_client/repositories/api/generic/user_repository.dart';
import 'package:pisec_client/services/auth_http_client.dart';

class HttpUserRepository implements UserRepository {
  final AuthHttpClient client;
  final String baseUrl;

  const HttpUserRepository(this.client, this.baseUrl);

  @override
  Future<CameraCredentialResponse> createCameraCredential() async {
    final response = await client.post(
      Uri(path: "$baseUrl/users/me/credential"),
    );
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to create a camera credential",
      );
    }
    return CameraCredentialResponse.fromJson(json.decode(response.body));
  }

  @override
  Future<UserResponse> deleteUser(int userId) async {
    final response = await client.delete(Uri(path: "$baseUrl/users/$userId"));
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to delete user",
      );
    }
    return UserResponse.fromJson(json.decode(response.body));
  }

  @override
  Future<UserResponse> getCurrentUser() async {
    final response = await client.get(Uri(path: "$baseUrl/users/me"));
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to get current user",
      );
    }
    return UserResponse.fromJson(json.decode(response.body));
  }

  @override
  Future<List<UserResponse>> getUsersByCamera(
    int cameraId, {
    PaginationParams pagination = const PaginationParams(),
  }) async {
    final String query =
        "${pagination.toPathQueryString()}&camera_id=$cameraId";
    final Uri url = Uri(path: "$baseUrl/users/?$query");

    final response = await client.get(url);
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to get users",
      );
    }
    return json
        .decode(response.body)
        .map((user) => UserResponse.fromJson(user))
        .toList();
  }

  @override
  Future<UserResponse> updateCurrentUser(UserQuery userQuery) async {
    final response = await client.put(
      Uri(path: "$baseUrl/users/me"),
      body: userQuery.toJson(),
    );
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to update current user",
      );
    }
    return UserResponse.fromJson(json.decode(response.body));
  }
}
