import 'package:pisec_client/models/api/queryables/camera_query.dart';
import 'package:pisec_client/models/api/queryables/pagination_params.dart';
import 'package:pisec_client/models/api/responses/camera_response.dart';
import 'package:pisec_client/models/api/responses/camera_subscription_response.dart';
import 'package:pisec_client/models/api/responses/paginated_response.dart';

abstract interface class CameraRepository {
  Future<PaginatedResponse<CameraResponse>> getCameras({
    PaginationParams pagination = const PaginationParams(),
    CameraQuery cameraQuery = const CameraQuery(),
  });

  Future<PaginatedResponse<CameraResponse>> getCamerasByUser(
    int userId, {
    PaginationParams pagination = const PaginationParams(),
  });

  Future<PaginatedResponse<CameraResponse>> getCurrentUserCameras({
    PaginationParams pagination = const PaginationParams(),
  });

  Future<CameraSubscriptionResponse> subscribeToCamera(
    int userId,
    int cameraId,
  );
}
