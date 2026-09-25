import 'package:flutter/material.dart';
import 'package:pisec_client/globals/notifier_provider.dart';
import 'package:pisec_client/repositories/api/generic/user_repository.dart';
import 'package:pisec_client/routes/route_args/credentials_route_args.dart';
import 'package:pisec_client/routes/route_args/profile_route_args.dart';
import 'package:pisec_client/viewmodels/auth_state.dart';

class SettingsPage extends StatelessWidget {
  final UserRepository userRepository;
  const SettingsPage({super.key, required this.userRepository});

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        ListTile(
          leading: Icon(Icons.account_circle),
          title: Text("Profile"),
          subtitle: Text("Change account details"),
          onTap: () => Navigator.pushNamed(
            context,
            '/profile',
            arguments: ProfileRouteArgs(
              userRepository: userRepository,
              initialEmail:
                  NotifierProvider.of<AuthState>(
                    context,
                    listen: false,
                  ).currentUser?.email ??
                  "",
            ),
          ),
        ),
        ListTile(
          leading: Icon(Icons.key),
          title: Text("Credentials"),
          subtitle: Text("Manage camera credentials"),
          onTap: () => Navigator.pushNamed(
            context,
            '/credentials',
            arguments: CredentialsRouteArgs(userRepository: userRepository),
          ),
        ),
        ListTile(
          leading: Icon(Icons.info),
          title: Text("About"),
          subtitle: Text("View app and server info"),
          onTap: () => Navigator.pushNamed(context, '/unfinished'),
        ),
        Center(
          child: FittedBox(
            child: Padding(
              padding: const EdgeInsets.all(8.0),
              child: TextButton(
                onPressed: () => _logout(context),
                style: ButtonStyle(
                  backgroundColor: WidgetStatePropertyAll<Color>(
                    Theme.of(context).colorScheme.errorContainer,
                  ),
                  foregroundColor: WidgetStatePropertyAll<Color>(
                    Theme.of(context).colorScheme.onErrorContainer,
                  ),
                ),
                child: Row(children: [Icon(Icons.logout), Text("Sign out")]),
              ),
            ),
          ),
        ),
      ],
    );
  }

  Future<void> _logout(BuildContext context) async {
    final authState = NotifierProvider.of<AuthState>(context);
    await authState.logout();
  }
}
