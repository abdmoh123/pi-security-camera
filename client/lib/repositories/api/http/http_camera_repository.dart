import 'dart:convert';

import 'package:pisec_client/exceptions/http_exceptions.dart';
import 'package:pisec_client/extensions/http.dart';
import 'package:pisec_client/models/api/queryables/camera_query.dart';
import 'package:pisec_client/models/api/queryables/pagination_params.dart';
import 'package:pisec_client/models/api/responses/camera_response.dart';
import 'package:pisec_client/models/api/responses/camera_subscription_response.dart';
import 'package:pisec_client/models/api/responses/paginated_response.dart';
import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/repositories/api/generic/camera_repository.dart';
import 'package:pisec_client/services/auth_http_client.dart';

class HttpCameraRepository implements CameraRepository {
  final AuthHttpClient client;
  final String baseUrl;

  const HttpCameraRepository(this.client, this.baseUrl);

  @override
  Future<PaginatedResponse<CameraResponse>> getCameras({
    PaginationParams pagination = const PaginationParams(),
    CameraQuery cameraQuery = const CameraQuery(),
  }) async {
    final query = PathQueryable.combineToPathQueryString([
      pagination,
      cameraQuery,
    ]);
    final Uri url = Uri.parse("$baseUrl/cameras/?$query");

    final response = await client.get(url);
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to get cameras.",
      );
    }

    return PaginatedResponse<CameraResponse>.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
      (camera) => CameraResponse.fromJson(camera),
    );
  }

  @override
  Future<PaginatedResponse<CameraResponse>> getCamerasByUser(
    int userId, {
    PaginationParams pagination = const PaginationParams(),
  }) async {
    final String query = "${pagination.toPathQueryString()}&user_id=$userId";
    final Uri url = Uri.parse("$baseUrl/cameras/?$query");

    final response = await client.get(url);
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to get cameras.",
      );
    }

    return PaginatedResponse<CameraResponse>.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
      (camera) => CameraResponse.fromJson(camera),
    );
  }

  @override
  Future<PaginatedResponse<CameraResponse>> getCurrentUserCameras({
    PaginationParams pagination = const PaginationParams(),
  }) async {
    final Uri url = Uri.parse(
      "$baseUrl/users/me/cameras/?${pagination.toPathQueryString()}",
    );

    final response = await client.get(url);
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to get current user's cameras.",
      );
    }

    return PaginatedResponse<CameraResponse>.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
      (camera) => CameraResponse.fromJson(camera),
    );
  }

  @override
  Future<CameraSubscriptionResponse> subscribeToCamera(
    int userId,
    int cameraId,
  ) async {
    final response = await client.post(
      Uri.parse("$baseUrl/users/$userId/subscriptions/$cameraId"),
    );
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to subscribe user $userId to camera $cameraId.",
      );
    }

    return CameraSubscriptionResponse.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
    );
  }
}
