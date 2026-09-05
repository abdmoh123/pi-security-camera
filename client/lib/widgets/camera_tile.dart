import 'package:flutter/material.dart';
import 'package:pisec_client/models/api/responses/camera_response.dart';

class CameraTile extends StatelessWidget {
  final CameraResponse camera;

  const CameraTile({super.key, required this.camera});

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
    );
  }
}
