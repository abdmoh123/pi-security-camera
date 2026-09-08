import 'package:flutter/material.dart';

class SettingsPage extends StatelessWidget {
  const SettingsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        ListTile(
          leading: Icon(Icons.account_circle),
          title: Text("Profile"),
          subtitle: Text("Change account details"),
          onTap: () => Navigator.pushNamed(context, '/unfinished'),
        ),
        ListTile(
          leading: Icon(Icons.key),
          title: Text("Credentials"),
          subtitle: Text("Manage camera credentials"),
          onTap: () => Navigator.pushNamed(context, '/unfinished'),
        ),
        ListTile(
          leading: Icon(Icons.notifications),
          title: Text("Notifications"),
          subtitle: Text("Adjust notification preferences"),
          onTap: () => Navigator.pushNamed(context, '/unfinished'),
        ),
        ListTile(
          leading: Icon(Icons.settings),
          title: Text("App settings"),
          subtitle: Text("Adjust preferences"),
          onTap: () => Navigator.pushNamed(context, '/unfinished'),
        ),
        ListTile(
          leading: Icon(Icons.help),
          title: Text("Help"),
          subtitle: Text("View tutorials and documentation"),
          onTap: () => Navigator.pushNamed(context, '/unfinished'),
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
                onPressed: () {},
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
}
