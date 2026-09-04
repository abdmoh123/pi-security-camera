import 'dart:async';

import 'package:flutter/material.dart';
import 'package:pisec_client/models/api/queryables/pagination_params.dart';
import 'package:pisec_client/models/api/responses/paginated_response.dart';
import 'package:pisec_client/models/api/responses/video_response.dart';
import 'package:pisec_client/repositories/api/generic/video_repository.dart';
import 'package:pisec_client/widgets/video_card.dart';

class VideosPage extends StatefulWidget {
  final VideoRepository videoRepository;

  const VideosPage({super.key, required this.videoRepository});

  @override
  State<StatefulWidget> createState() => _VideosPageState();
}

class _VideosPageState extends State<VideosPage> {
  Future<PaginatedResponse<VideoResponse>> futureVideos = Future.value(
    PaginatedResponse<VideoResponse>.empty(),
  );

  int currentPage = 1;
  int maxPages = 1;

  @override
  void initState() {
    super.initState();
    _refreshVideos();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Container(
          padding: EdgeInsetsGeometry.all(8.0),
          child: Text("Videos", textAlign: TextAlign.center),
        ),
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(mainAxisAlignment: MainAxisAlignment.start),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              spacing: 8.0,
              children: [_buildPaginationGroup(context)],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              spacing: 8.0,
              children: [
                IconButton(
                  onPressed: _refreshVideos,
                  icon: Icon(Icons.refresh),
                ),
              ],
            ),
          ],
        ),
        Expanded(
          child: FutureBuilder(
            future: futureVideos,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(child: CircularProgressIndicator());
              }
              if (snapshot.hasError) {
                return Center(child: Text(snapshot.error.toString()));
              }
              if (snapshot.hasData) {
                if (snapshot.data!.items.isEmpty) {
                  return const Center(child: Text("No videos found"));
                }
                return _buildVideoList(snapshot.data!.items);
              }
              return const Center(child: Text("Something went wrong"));
            },
          ),
        ),
      ],
    );
  }

  Widget _buildPaginationGroup(BuildContext context) {
    List<Widget> children = [];

    final toFirstPage = currentPage == 1 ? null : () => _toPage(1);
    final toPreviousPage = currentPage == 1 ? null : _previousPage;
    children.add(TextButton(onPressed: toFirstPage, child: Text("<<")));
    children.add(TextButton(onPressed: toPreviousPage, child: Text("<")));

    if (currentPage > 2) {
      children.add(
        TextButton(
          onPressed: () => _toPage(currentPage - 2),
          child: Text((currentPage - 2).toString()),
        ),
      );
    }
    if (currentPage > 1) {
      children.add(
        TextButton(
          onPressed: () => _toPage(currentPage - 1),
          child: Text((currentPage - 1).toString()),
        ),
      );
    }

    children.add(
      TextButton(
        onPressed: () => _toPage(currentPage),
        style: ButtonStyle(
          backgroundColor: WidgetStatePropertyAll<Color>(
            Theme.of(context).colorScheme.inversePrimary,
          ),
        ),
        child: Text(currentPage.toString()),
      ),
    );

    if (currentPage < maxPages - 1) {
      children.add(
        TextButton(
          onPressed: () => _toPage(currentPage + 1),
          child: Text((currentPage + 1).toString()),
        ),
      );
    }
    if (currentPage < maxPages - 2) {
      children.add(
        TextButton(
          onPressed: () => _toPage(currentPage + 2),
          child: Text((currentPage + 2).toString()),
        ),
      );
    }

    final toLastPage = currentPage == maxPages ? null : () => _toPage(maxPages);
    final toNextPage = currentPage == maxPages ? null : _nextPage;
    children.add(TextButton(onPressed: toNextPage, child: Text(">")));
    children.add(TextButton(onPressed: toLastPage, child: Text(">>")));

    return Row(children: children);
  }

  Widget _buildVideoList(List<VideoResponse> videos) {
    return ListView.builder(
      itemCount: videos.length,
      itemBuilder: (context, index) {
        return VideoCard(
          video: videos[index],
          downloadVideo: () =>
              widget.videoRepository.downloadVideo(videos[index].id),
          deleteVideo: () {
            final result = widget.videoRepository.deleteVideo(videos[index].id);
            result.then((response) => _refreshVideos());
            return result;
          },
        );
      },
    );
  }

  Future<PaginatedResponse<VideoResponse>> _getAllVideos({
    int? page,
    int pageSize = 10,
  }) async {
    page = page ?? currentPage;
    return widget.videoRepository.getVideos(
      pagination: PaginationParams(pageIndex: page - 1, pageSize: pageSize),
    );
  }

  void _toPage(int page) {
    if (page == currentPage) {
      return;
    }
    setState(() {
      currentPage = page;
      futureVideos = _getAllVideos();
      futureVideos.then((response) => maxPages = response.totalPages);
    });
  }

  void _nextPage() {
    if (currentPage == maxPages) {
      return;
    }
    _toPage(currentPage + 1);
  }

  void _previousPage() {
    if (currentPage == 1) {
      return;
    }
    _toPage(currentPage - 1);
  }

  void _refreshVideos() {
    setState(() {
      futureVideos = _getAllVideos();
      futureVideos.then((response) => maxPages = response.totalPages);
    });
  }
}
