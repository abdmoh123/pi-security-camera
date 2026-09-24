import 'package:flutter/material.dart';
import 'package:pisec_client/exceptions/http_exceptions.dart';
import 'package:pisec_client/globals/notifier_provider.dart';
import 'package:pisec_client/models/api/queryables/user_query.dart';
import 'package:pisec_client/repositories/api/generic/user_repository.dart';
import 'package:pisec_client/viewmodels/auth_state.dart';

class ProfilePage extends StatefulWidget {
  final UserRepository userRepository;
  final String initialEmail;

  const ProfilePage({
    super.key,
    required this.userRepository,
    this.initialEmail = "",
  });

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  bool _passwordHidden = true;

  @override
  void initState() {
    super.initState();
    _emailController.text = widget.initialEmail;
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    const spacing = 12.0;

    return Scaffold(
      appBar: AppBar(title: const Text("Profile")),
      body: Form(
        child: Padding(
          padding: const EdgeInsets.all(spacing),
          child: Center(
            child: ConstrainedBox(
              constraints: const BoxConstraints(maxWidth: 400),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  TextFormField(
                    decoration: const InputDecoration(
                      labelText: 'User email',
                      border: OutlineInputBorder(),
                    ),
                    controller: _emailController,
                    onFieldSubmitted: (_) => _onSubmit(context),
                  ),
                  const SizedBox(height: spacing),
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
                  const SizedBox(height: spacing),
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
                    child: const Text("Update profile"),
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
    if (_passwordController.text != _confirmPasswordController.text) {
      // TODO: Display error message via toast or popup
      return;
    }

    // TODO: Handle invalid emails
    final String? emailText = _emailController.text == widget.initialEmail
        ? null
        : (_emailController.text.isEmpty ? null : _emailController.text);
    final query = UserQuery(
      email: emailText,
      password: _passwordController.text,
    );

    try {
      await widget.userRepository.updateCurrentUser(query);
    } on HttpCodedException {
      // If user details haven't changed, then there is nothing to do
      return;
    } catch (e) {
      // TODO: Display error message via toast or popup
    }

    if (emailText != null) {
      // Required because we are using context more than once in async
      if (!context.mounted) return;

      final authState = NotifierProvider.of<AuthState>(context);
      await authState.reLogin(
        UserQuery(email: emailText, password: _passwordController.text),
      );
    }

    // Required because we are using context more than once in async
    if (!context.mounted) return;

    Navigator.pop(context);
  }
}
