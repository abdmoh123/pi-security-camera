import 'package:flutter/material.dart';
import 'package:pisec_client/models/api/responses/camera_response.dart';

class CameraCard extends StatelessWidget {
  final CameraResponse camera;

  const CameraCard({super.key, required this.camera});

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Container(
        padding: const EdgeInsets.all(8.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.start,
          spacing: 8.0,
          children: [
            Container(
              padding: const EdgeInsets.all(20.0),
              decoration: BoxDecoration(
                color: Theme.of(context).colorScheme.primaryContainer,
                border: Border.all(
                  color: Theme.of(context).colorScheme.inversePrimary,
                ),
                borderRadius: BorderRadius.circular(8.0),
              ),
              child: Icon(Icons.videocam, size: 38.0),
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              spacing: 2.0,
              children: [
                Text(
                  camera.name,
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      "id: ${camera.id}",
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                    Text(
                      "mac address: ${camera.macAddress}",
                      style: Theme.of(context).textTheme.bodyMedium,
                    ),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
