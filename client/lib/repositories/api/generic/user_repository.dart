import 'package:pisec_client/models/api/queryables/pagination_params.dart';
import 'package:pisec_client/models/api/queryables/user_query.dart';
import 'package:pisec_client/models/api/responses/camera_credential_response.dart';
import 'package:pisec_client/models/api/responses/user_response.dart';

abstract interface class UserRepository {
  Future<UserResponse> createUser(String email, String password);

  Future<UserResponse> deleteUser(int userId);

  Future<UserResponse> getCurrentUser();

  Future<List<UserResponse>> getUsersByCamera(
    int cameraId, {
    PaginationParams pagination = const PaginationParams(),
  });

  Future<UserResponse> updateCurrentUser(UserQuery userQuery);

  Future<CameraCredentialResponse> createCameraCredential();
}
