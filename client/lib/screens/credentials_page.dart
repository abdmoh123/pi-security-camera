import 'package:flutter/material.dart';
import 'package:pisec_client/models/api/queryables/pagination_params.dart';
import 'package:pisec_client/models/api/responses/paginated_response.dart';
import 'package:pisec_client/models/api/responses/redacted_camera_credential_response.dart';
import 'package:pisec_client/repositories/api/generic/user_repository.dart';
import 'package:pisec_client/widgets/credential_tile.dart';

class CredentialsPage extends StatefulWidget {
  final UserRepository userRepository;

  const CredentialsPage({super.key, required this.userRepository});

  @override
  State<StatefulWidget> createState() => _CredetialsPageState();
}

class _CredetialsPageState extends State<CredentialsPage> {
  Future<PaginatedResponse<RedactedCameraCredentialResponse>> future =
      Future.value(PaginatedResponse<RedactedCameraCredentialResponse>.empty());

  @override
  void initState() {
    super.initState();
    _refreshCredentials();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Credentials")),
      floatingActionButton: FloatingActionButton(
        child: Icon(Icons.add),
        onPressed: () => _newCredential(),
      ),
      body: FutureBuilder(
        future: future,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text(snapshot.error.toString()));
          }
          if (snapshot.hasData) {
            if (snapshot.data!.items.isEmpty) {
              return const Center(child: Text("No credentials found"));
            }
            return _buildCredentialsList(snapshot.data!.items);
          }
          return const Center(child: Text("Something went wrong"));
        },
      ),
    );
  }

  Widget _buildCredentialsList(
    List<RedactedCameraCredentialResponse> credentials,
  ) {
    return ListView.separated(
      itemCount: credentials.length,
      itemBuilder: (context, index) {
        return CredentialTile(credential: credentials[index]);
      },
      separatorBuilder: (context, index) => Divider(),
    );
  }

  Future<PaginatedResponse<RedactedCameraCredentialResponse>>
  _getCredentials() async {
    try {
      final response = await widget.userRepository.getCameraCredentials(
        PaginationParams(pageIndex: 0, pageSize: 1000),
      );
      return response;
    } catch (e, st) {
      return Future.error(e, st);
    }
  }

  void _refreshCredentials() {
    setState(() {
      future = _getCredentials();
    });
  }

  void _newCredential() {
    // TODO: Implement this
    throw UnimplementedError();
  }
}
