import 'package:flutter/material.dart';
import 'package:pisec_client/globals/auth_state_scope.dart';
import 'package:pisec_client/models/api/queryables/user_query.dart';

class LoginPage extends StatefulWidget {
  final String initialServerUrl;
  final String initialEmail;

  const LoginPage({
    super.key,
    this.initialServerUrl = "",
    this.initialEmail = "",
  });

  @override
  State<StatefulWidget> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final _serverUrlController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  initState() {
    super.initState();
    _serverUrlController.text = widget.initialServerUrl;
    _emailController.text = widget.initialEmail;
  }

  @override
  dispose() {
    _serverUrlController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Pisec - Login")),
      body: Form(
        child: Column(
          children: [
            TextFormField(
              decoration: InputDecoration(
                labelText: 'Server host',
                border: OutlineInputBorder(),
              ),
              controller: _serverUrlController,
            ),
            TextFormField(
              decoration: InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
              ),
              controller: _emailController,
            ),
            TextFormField(
              decoration: InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
              controller: _passwordController,
              obscureText: true,
            ),
            ElevatedButton(
              onPressed: () => _onSubmit(context),
              child: Text("Login"),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _onSubmit(BuildContext context) async {
    final userQuery = UserQuery(
      email: _emailController.text,
      password: _passwordController.text,
    );

    final authState = AuthStateScope.of(context);
    await authState.login(_serverUrlController.text, userQuery);

    // Required because we are using context more than once
    if (!context.mounted) {
      return;
    }

    if (!authState.isAuthenticated) {
      _passwordController.clear();
      return;
    }

    Navigator.of(context).pushNamedAndRemoveUntil("/", (route) => false);
  }
}
