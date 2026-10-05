import 'dart:convert';

import 'package:http/http.dart';
import 'package:pisec_client/exceptions/http_exceptions.dart';
import 'package:pisec_client/extensions/http.dart';
import 'package:pisec_client/models/api/queryables/camera_query.dart';
import 'package:pisec_client/models/api/queryables/pagination_params.dart';
import 'package:pisec_client/models/api/responses/camera_response.dart';
import 'package:pisec_client/models/api/responses/camera_subscription_response.dart';
import 'package:pisec_client/models/api/responses/paginated_response.dart';
import 'package:pisec_client/models/api/sortables/camera_fields.dart';
import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/models/sortable.dart';
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
    bool onlyOwned = false,
    Sortable<CameraFields>? orderBy,
    PaginationParams pagination = const PaginationParams(),
  }) async {
    final orderByString = orderBy == null
        ? ""
        : "&order_by=${orderBy.toString()}";
    final Uri url = Uri.parse(
      "$baseUrl/users/me/cameras/?${pagination.toPathQueryString()}&only_owned=$onlyOwned$orderByString",
    );

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
    late final Response response;
    try {
      response = await client.post(
        Uri.parse("$baseUrl/users/$userId/subscriptions/$cameraId"),
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
        message: "Failed to subscribe user $userId to camera $cameraId.",
      );
    }

    return CameraSubscriptionResponse.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
    );
  }

  @override
  Future<CameraSubscriptionResponse> unsubscribeFromCamera(
    int userId,
    int cameraId,
  ) async {
    late final Response response;
    try {
      response = await client.delete(
        Uri.parse("$baseUrl/users/$userId/subscriptions/$cameraId"),
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
        message: "Failed to unsubscribe user $userId from camera $cameraId.",
      );
    }

    return CameraSubscriptionResponse.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
    );
  }
}
