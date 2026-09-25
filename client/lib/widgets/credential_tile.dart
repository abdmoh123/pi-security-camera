import 'package:flutter/material.dart';
import 'package:pisec_client/models/api/responses/redacted_camera_credential_response.dart';

class CredentialTile extends StatelessWidget {
  final RedactedCameraCredentialResponse credential;
  final bool isUnread;

  const CredentialTile({
    super.key,
    required this.credential,
    this.isUnread = true,
  });

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
        credential.cameraID?.toString() ?? "Unassigned",
        textAlign: TextAlign.left,
        maxLines: 1,
        overflow: TextOverflow.ellipsis,
      ),
    );
  }
}
