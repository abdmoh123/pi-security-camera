import 'package:flutter/material.dart';
import 'package:pisec_client/models/api/queryables/pagination_params.dart';
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
  Future<List<VideoResponse>> futureVideos = Future.value([]);

  int currentPage = 1;
  int maxPages = 10; // TODO: Get the actual value from server

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
                if (snapshot.data!.isEmpty) {
                  return const Center(child: Text("No videos found"));
                }
                return _buildVideoList(snapshot.data!);
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

    children.add(TextButton(onPressed: () => _toPage(1), child: Text("<<")));
    children.add(TextButton(onPressed: _previousPage, child: Text("<")));

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

    children.add(TextButton(onPressed: _nextPage, child: Text(">")));
    children.add(
      TextButton(onPressed: () => _toPage(maxPages), child: Text(">>")),
    );

    return Row(children: children);
  }

  Widget _buildVideoList(List<VideoResponse> videos) {
    return ListView.builder(
      itemCount: videos.length,
      itemBuilder: (context, index) {
        return VideoCard(video: videos[index]);
      },
    );
  }

  Future<List<VideoResponse>> _getAllVideos({
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
    });
  }
}
