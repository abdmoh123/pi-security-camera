import 'package:flutter/material.dart';
import 'package:pisec_client/models/api/responses/camera_response.dart';

enum _CameraTileActions { subscribe, unsubscribe }

class CameraTile extends StatelessWidget {
  final Future<void> Function(CameraResponse camera)? _subscribeToCamera;
  final Future<void> Function(CameraResponse camera)? _unsubscribeFromCamera;

  final CameraResponse camera;

  const CameraTile({
    super.key,
    required this.camera,
    Future<void> Function(CameraResponse camera)? subscribeToCamera,
    Future<void> Function(CameraResponse camera)? unSubscribeToCamera,
  }) : _subscribeToCamera = subscribeToCamera,
       _unsubscribeFromCamera = unSubscribeToCamera;

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
        onSelected: (value) async {
          switch (value) {
            case _CameraTileActions.subscribe:
              await _subscribeToCamera!(camera);
            case _CameraTileActions.unsubscribe:
              await _unsubscribeFromCamera!(camera);
          }
        },
        itemBuilder: (context) => [
          PopupMenuItem(
            enabled: _subscribeToCamera != null,
            value: _CameraTileActions.subscribe,
            child: Text("Subscribe"),
          ),
          PopupMenuItem(
            enabled: _unsubscribeFromCamera != null,
            value: _CameraTileActions.unsubscribe,
            child: Text("Unsubscribe"),
          ),
        ],
      ),
    );
  }
}
