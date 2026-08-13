import 'package:pisec_client/models/api/queryables/pagination_params.dart';
import 'package:pisec_client/models/api/queryables/video_query.dart';
import 'package:pisec_client/models/api/responses/video_response.dart';

abstract class VideoRepository {
  Future<VideoResponse> deleteVideo(int userId);

  Future<VideoResponse> getVideo(int videoId);

  Future<List<VideoResponse>> getVideos({
    PaginationParams pagination = const PaginationParams(),
    VideoQuery videoQuery = const VideoQuery(),
  });

  Future<List<VideoResponse>> getVideosByCamera(
    int cameraId, {
    PaginationParams pagination = const PaginationParams(),
  });
}
