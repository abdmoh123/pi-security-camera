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

  bool _passwordHidden = true;

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
    const spacing = 12.0;
    return Scaffold(
      appBar: AppBar(title: Text("Pisec - Login")),
      body: Form(
        child: Padding(
          padding: const EdgeInsets.all(spacing),
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 400),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                spacing: spacing,
                children: [
                  Text(
                    "Sign in to your Pisec server",
                    style: Theme.of(context).textTheme.headlineMedium,
                  ),
                  const SizedBox(height: 2 * spacing),
                  TextFormField(
                    decoration: const InputDecoration(
                      labelText: 'Server host',
                      border: OutlineInputBorder(),
                    ),
                    controller: _serverUrlController,
                  ),
                  const SizedBox(height: spacing),
                  TextFormField(
                    decoration: const InputDecoration(
                      labelText: 'Email',
                      border: OutlineInputBorder(),
                    ),
                    controller: _emailController,
                  ),
                  TextFormField(
                    decoration: InputDecoration(
                      labelText: 'Password',
                      border: const OutlineInputBorder(),
                      suffixIcon: IconButton(
                        onPressed: () =>
                            setState(() => _passwordHidden = !_passwordHidden),
                        icon: Icon(
                          _passwordHidden
                              ? Icons.visibility
                              : Icons.visibility_off,
                        ),
                        tooltip: _passwordHidden
                            ? "Show password"
                            : "Hide password",
                      ),
                    ),
                    controller: _passwordController,
                    obscureText: _passwordHidden,
                  ),
                  const SizedBox(height: spacing),
                  FilledButton(
                    onPressed: () => _onSubmit(context),
                    child: const Text("Sign in"),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Future<void> _onSubmit(BuildContext context) async {
    final userQuery = UserQuery(
      email: _emailController.text,
      password: _passwordController.text,
    );

    // TODO: Improve how invalid input is handled
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
