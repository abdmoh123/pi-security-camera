import 'package:flutter/material.dart';
import 'package:pisec_client/models/api/responses/camera_response.dart';

enum _CameraTileActions { subscribe }

class CameraTile extends StatelessWidget {
  final Future<void> Function(int cameraID) _subscribeToCamera;

  final CameraResponse camera;

  const CameraTile({
    super.key,
    required this.camera,
    required Future<void> Function(int cameraID) subscribeToCamera,
  }) : _subscribeToCamera = subscribeToCamera;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Container(
        padding: const EdgeInsets.all(12.0),
        decoration: BoxDecoration(
          color: Theme.of(context).colorScheme.primaryContainer,
          border: Border.all(
            color: Theme.of(context).colorScheme.inversePrimary,
          ),
          borderRadius: BorderRadius.circular(8.0),
        ),
        child: Icon(Icons.videocam),
      ),
      title: Text(camera.name, maxLines: 1, overflow: TextOverflow.ellipsis),
      subtitle: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            "id: ${camera.id}",
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
          Text(
            "mac address: ${camera.macAddress}",
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
      trailing: PopupMenuButton<_CameraTileActions>(
        onSelected: (value) {
          switch (value) {
            case _CameraTileActions.subscribe:
              _subscribeToCamera(camera.id);
          }
        },
        itemBuilder: (context) => [
          const PopupMenuItem(
            value: _CameraTileActions.subscribe,
            child: Text("Subscribe"),
          ),
        ],
      ),
    );
  }
}
