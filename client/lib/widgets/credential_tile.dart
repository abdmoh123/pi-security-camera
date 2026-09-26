import 'package:flutter/material.dart';
import 'package:pisec_client/models/api/responses/redacted_camera_credential_response.dart';

class CredentialTile extends StatelessWidget {
  final RedactedCameraCredentialResponse credential;
  final bool isUnread;
  final Future<void> Function()? _deleteCredential;

  const CredentialTile({
    super.key,
    required this.credential,
    Future<void> Function()? deleteCredential,
    this.isUnread = true,
  }) : _deleteCredential = deleteCredential;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: const Icon(Icons.key),
      title: Text(
        credential.clientID,
        textAlign: TextAlign.left,
        maxLines: 1,
        overflow: TextOverflow.ellipsis,
      ),
      subtitle: Text(
        "camera-id: ${credential.cameraID?.toString() ?? "Unassigned"}",
        textAlign: TextAlign.left,
        maxLines: 1,
        overflow: TextOverflow.ellipsis,
      ),
      // Add delete button if a delete callback is provided
      trailing: _deleteCredential == null
          ? null
          : IconButton(
              onPressed: () => _onDelete(),
              icon: const Icon(Icons.delete),
            ),
    );
  }

  Future<void> _onDelete() async {
    try {
      await _deleteCredential?.call();
    } catch (e, st) {
      return Future.error(e, st);
    }
  }
}
