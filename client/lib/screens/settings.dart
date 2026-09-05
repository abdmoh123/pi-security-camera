import 'package:flutter/material.dart';

class Settings extends StatelessWidget {
  const Settings({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: [
        ListTile(
          leading: Icon(Icons.account_circle),
          title: Text("Profile"),
          subtitle: Text("Change account details"),
        ),
        ListTile(
          leading: Icon(Icons.key),
          title: Text("Credentials"),
          subtitle: Text("Manage camera credentials"),
        ),
        ListTile(
          leading: Icon(Icons.notifications),
          title: Text("Notifications"),
          subtitle: Text("Adjust notification preferences"),
        ),
        ListTile(
          leading: Icon(Icons.settings),
          title: Text("App settings"),
          subtitle: Text("Adjust preferences"),
        ),
        ListTile(
          leading: Icon(Icons.help),
          title: Text("Help"),
          subtitle: Text("View tutorials and documentation"),
        ),
        ListTile(
          leading: Icon(Icons.info),
          title: Text("About"),
          subtitle: Text("View app and server info"),
        ),
        Center(
          child: FittedBox(
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
      ],
    );
  }
}
