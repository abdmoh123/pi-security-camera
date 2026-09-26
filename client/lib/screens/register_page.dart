import 'package:flutter/material.dart';
import 'package:pisec_client/models/api/queryables/user_query.dart';
import 'package:pisec_client/routes/route_args/login_route_args.dart';
import 'package:pisec_client/services/login_api_service.dart';

class RegisterPage extends StatefulWidget {
  final LoginAPIService authService;
  final String initialServerUrl;
  final String initialEmail;

  const RegisterPage({
    super.key,
    required this.authService,
    this.initialServerUrl = "",
    this.initialEmail = "",
  });

  @override
  State<StatefulWidget> createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _serverUrlController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

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
    _confirmPasswordController.dispose();
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
                    onFieldSubmitted: (_) => _onSubmit(context),
                  ),
                  const SizedBox(height: spacing),
                  TextFormField(
                    decoration: const InputDecoration(
                      labelText: 'Email',
                      border: OutlineInputBorder(),
                    ),
                    controller: _emailController,
                    onFieldSubmitted: (_) => _onSubmit(context),
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
                    onFieldSubmitted: (_) => _onSubmit(context),
                  ),
                  TextFormField(
                    decoration: InputDecoration(
                      labelText: 'Confirm password',
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
                    controller: _confirmPasswordController,
                    obscureText: _passwordHidden,
                    onFieldSubmitted: (_) => _onSubmit(context),
                  ),
                  const SizedBox(height: spacing),
                  FilledButton(
                    onPressed: () => _onSubmit(context),
                    child: const Text("Register"),
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
    // TODO: Display error message via toast or popup
    if (_passwordController.text != _confirmPasswordController.text) return;

    final userQuery = UserQuery(
      email: _emailController.text,
      password: _passwordController.text,
    );

    // Required because we are using context more than once in async
    if (!context.mounted) return;

    try {
      final response = await widget.authService.registerUser(userQuery);

      // Required because we are using context more than once in async
      if (!context.mounted) return;

      // Go to the login page with same email and server address filled in
      Navigator.of(context).pushNamedAndRemoveUntil(
        "/login",
        (route) => false,
        arguments: LoginRouteArgs(
          serverUrl: _serverUrlController.text,
          email: response.email,
        ),
      );
    } catch (e, st) {
      return Future.error(e, st);
    }
  }
}
