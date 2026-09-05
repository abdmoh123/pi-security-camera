import 'package:flutter/material.dart';
import 'package:pisec_client/models/api/queryables/pagination_params.dart';
import 'package:pisec_client/models/api/responses/camera_response.dart';
import 'package:pisec_client/models/api/responses/paginated_response.dart';
import 'package:pisec_client/repositories/api/generic/camera_repository.dart';
import 'package:pisec_client/widgets/camera_card.dart';

class CamerasPage extends StatefulWidget {
  final CameraRepository cameraRepository;

  const CamerasPage({super.key, required this.cameraRepository});

  @override
  State<StatefulWidget> createState() => _CamerasPageState();
}

class _CamerasPageState extends State<CamerasPage> {
  Future<PaginatedResponse<CameraResponse>> futureCameras = Future.value(
    PaginatedResponse<CameraResponse>.empty(),
  );

  int currentPage = 1;
  int maxPages = 1;

  @override
  void initState() {
    super.initState();
    _refreshCameras();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Container(
          padding: EdgeInsetsGeometry.all(8.0),
          child: Text("Cameras", textAlign: TextAlign.center),
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
                  onPressed: _refreshCameras,
                  icon: Icon(Icons.refresh),
                ),
              ],
            ),
          ],
        ),
        Expanded(
          child: FutureBuilder(
            future: futureCameras,
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
                return _buildCameraList(snapshot.data!.items);
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
    children.add(
      IconButton(onPressed: toFirstPage, icon: Icon(Icons.first_page)),
    );
    children.add(
      IconButton(onPressed: toPreviousPage, icon: Icon(Icons.chevron_left)),
    );

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
    children.add(
      IconButton(onPressed: toNextPage, icon: Icon(Icons.chevron_right)),
    );
    children.add(
      IconButton(onPressed: toLastPage, icon: Icon(Icons.last_page)),
    );

    return Row(children: children);
  }

  Widget _buildCameraList(List<CameraResponse> cameras) {
    return ListView.builder(
      itemCount: cameras.length,
      itemBuilder: (context, index) {
        return CameraCard(camera: cameras[index]);
      },
    );
  }

  Future<PaginatedResponse<CameraResponse>> _getAllCameras({
    int? page,
    int pageSize = 10,
  }) async {
    page = page ?? currentPage;
    return widget.cameraRepository.getCurrentUserCameras(
      pagination: PaginationParams(pageIndex: page - 1, pageSize: pageSize),
    );
  }

  void _toPage(int page) {
    if (page == currentPage) {
      return;
    }
    setState(() {
      currentPage = page;
      futureCameras = _getAllCameras();
      futureCameras.then((response) => maxPages = response.totalPages);
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

  void _refreshCameras() {
    setState(() {
      futureCameras = _getAllCameras();
      futureCameras.then((response) => maxPages = response.totalPages);
    });
  }
}
