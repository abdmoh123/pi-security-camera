import 'dart:convert';

import 'package:pisec_client/exceptions/http_exceptions.dart';
import 'package:pisec_client/extensions/http.dart';
import 'package:pisec_client/models/api/queryables/pagination_params.dart';
import 'package:pisec_client/models/api/queryables/video_query.dart';
import 'package:pisec_client/models/api/responses/paginated_response.dart';
import 'package:pisec_client/models/api/responses/video_response.dart';
import 'package:pisec_client/models/api/responses/video_url_response.dart';
import 'package:pisec_client/models/event_task.dart';
import 'package:pisec_client/models/http/http_queryable.dart';
import 'package:pisec_client/repositories/api/generic/video_repository.dart';
import 'package:pisec_client/services/auth_http_client.dart';
import 'package:pisec_client/services/download/downloader_service.dart';

class HttpVideoRepository implements VideoRepository {
  final AuthHttpClient client;
  final String baseUrl;
  final DownloaderService downloaderService;

  const HttpVideoRepository(this.client, this.baseUrl, this.downloaderService);

  @override
  Future<bool> cancelVideoDownload(EventTask downloadTask) =>
      downloaderService.cancelDownload(downloadTask);

  @override
  Future<VideoResponse> deleteVideo(int videoId) async {
    final response = await client.delete(Uri.parse("$baseUrl/videos/$videoId"));
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to delete video",
      );
    }

    return VideoResponse.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
    );
  }

  @override
  Future<EventTask?> downloadVideo(int videoId) async {
    final downloadUrlResponse = await client.get(
      Uri.parse("$baseUrl/$videoId/url"),
    );

    if (downloadUrlResponse.notOk) {
      throw HttpCodedException(
        statusCode: downloadUrlResponse.statusCode,
        message: "Failed to get video url",
      );
    }

    final downloadUrlObj = VideoUrlResponse.fromJson(
      json.decode(downloadUrlResponse.body) as Map<String, dynamic>,
    );

    return downloaderService.downloadItem(downloadUrlObj.url, "video.mp4");
  }

  @override
  Future<VideoResponse> getVideo(int videoId) async {
    final response = await client.get(Uri(path: "$baseUrl/videos/$videoId"));
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to get video",
      );
    }

    return VideoResponse.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
    );
  }

  @override
  Future<PaginatedResponse<VideoResponse>> getVideos({
    PaginationParams pagination = const PaginationParams(),
    VideoQuery videoQuery = const VideoQuery(),
  }) async {
    final String query = PathQueryable.combineToPathQueryString([
      pagination,
      videoQuery,
    ]);
    final Uri url = Uri.parse("$baseUrl/videos/?$query");

    final response = await client.get(url);
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to get videos",
      );
    }

    return PaginatedResponse<VideoResponse>.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
      (video) => VideoResponse.fromJson(video),
    );
  }

  @override
  Future<PaginatedResponse<VideoResponse>> getVideosByCamera(
    int cameraId, {
    PaginationParams pagination = const PaginationParams(),
  }) async {
    final String query =
        "${pagination.toPathQueryString()}&camera_id=$cameraId";
    final Uri url = Uri.parse("$baseUrl/videos/?$query");

    final response = await client.get(url);
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to get videos",
      );
    }

    return PaginatedResponse<VideoResponse>.fromJson(
      json.decode(response.body) as Map<String, dynamic>,
      (video) => VideoResponse.fromJson(video),
    );
  }
}
