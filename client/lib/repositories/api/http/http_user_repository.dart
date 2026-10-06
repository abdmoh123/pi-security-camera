import 'dart:convert';

import 'package:http/http.dart';
import 'package:pisec_client/constants/http/content_type_headers.dart';
import 'package:pisec_client/exceptions/http_exceptions.dart';
import 'package:pisec_client/extensions/http.dart';
import 'package:pisec_client/models/api/queryables/pagination_params.dart';
import 'package:pisec_client/models/api/queryables/user_query.dart';
import 'package:pisec_client/models/api/responses/camera_credential_response.dart';
import 'package:pisec_client/models/api/responses/paginated_response.dart';
import 'package:pisec_client/models/api/responses/redacted_camera_credential_response.dart';
import 'package:pisec_client/models/api/responses/user_response.dart';
import 'package:pisec_client/repositories/api/generic/user_repository.dart';
import 'package:pisec_client/services/auth_http_client.dart';

class HttpUserRepository implements UserRepository {
  final AuthHttpClient client;
  final String baseUrl;

  const HttpUserRepository(this.client, this.baseUrl);

  @override
  Future<CameraCredentialResponse> createCameraCredential() async {
    late final Response response;
    try {
      response = await client.post(Uri.parse("$baseUrl/users/me/credentials"));
    } catch (e) {
      throw HttpClientException(
        "Error occurred while calling server",
        inner: e,
      );
    }

    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to create a camera credential",
      );
    }

    return CameraCredentialResponse.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
    );
  }

  @override
  Future<RedactedCameraCredentialResponse> deleteCameraCredential(
    String clientId,
  ) async {
    late final Response response;
    try {
      response = await client.delete(
        Uri.parse("$baseUrl/users/me/credentials/$clientId"),
      );
    } catch (e) {
      throw HttpClientException(
        "Error occurred while calling server",
        inner: e,
      );
    }

    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to delete camera credential",
      );
    }

    return RedactedCameraCredentialResponse.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
    );
  }

  @override
  Future<UserResponse> deleteCurrentUser() async {
    late final Response response;
    try {
      response = await client.delete(Uri.parse("$baseUrl/users/me"));
    } catch (e) {
      throw HttpClientException(
        "Error occurred while calling server",
        inner: e,
      );
    }

    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to delete user",
      );
    }

    return UserResponse.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
    );
  }

  @override
  Future<PaginatedResponse<RedactedCameraCredentialResponse>>
  getCameraCredentials(PaginationParams pagination) async {
    final String query = pagination.toPathQueryString();

    late final Response response;
    try {
      response = await client.get(
        Uri.parse("$baseUrl/users/me/credentials?$query"),
      );
    } catch (e) {
      throw HttpClientException(
        "Error occurred while calling server",
        inner: e,
      );
    }

    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to get camera credentials",
      );
    }

    return PaginatedResponse<RedactedCameraCredentialResponse>.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
      (credential) => RedactedCameraCredentialResponse.fromJson(credential),
    );
  }

  @override
  Future<UserResponse> getCurrentUser() async {
    late final Response response;
    try {
      response = await client.get(Uri.parse("$baseUrl/users/me"));
    } catch (e) {
      throw HttpClientException(
        "Error occurred while calling server",
        inner: e,
      );
    }

    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to get current user",
      );
    }

    return UserResponse.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
    );
  }

  @override
  Future<PaginatedResponse<UserResponse>> getUsersByCamera(
    int cameraId, {
    PaginationParams pagination = const PaginationParams(),
  }) async {
    final String query =
        "${pagination.toPathQueryString()}&camera_id=$cameraId";
    final Uri url = Uri.parse("$baseUrl/users/?$query");

    late final Response response;
    try {
      response = await client.get(url);
    } catch (e) {
      throw HttpClientException(
        "Error occurred while calling server",
        inner: e,
      );
    }

    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to get users",
      );
    }

    return PaginatedResponse<UserResponse>.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
      (user) => UserResponse.fromJson(user),
    );
  }

  @override
  Future<UserResponse> updateCurrentUser(UserQuery userQuery) async {
    late final Response response;
    try {
      response = await client.put(
        Uri.parse("$baseUrl/users/me"),
        headers: jsonHeader.toDict(),
        body: json.encode(userQuery.toJson()),
      );
    } catch (e) {
      throw HttpClientException(
        "Error occurred while calling server",
        inner: e,
      );
    }

    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to update current user",
      );
    }

    return UserResponse.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
    );
  }

  @override
  Future<PaginatedResponse<UserResponse>> getUsersByName(
    String username, {
    PaginationParams pagination = const PaginationParams(),
  }) async {
    final String query = "${pagination.toPathQueryString()}&email=$username";
    final Uri url = Uri.parse("$baseUrl/users/?$query");

    late final Response response;
    try {
      response = await client.get(url);
    } catch (e) {
      throw HttpClientException(
        "Error occurred while calling server",
        inner: e,
      );
    }

    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to find users similar to username: $username",
      );
    }

    return PaginatedResponse<UserResponse>.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
      (user) => UserResponse.fromJson(user),
    );
  }
}
