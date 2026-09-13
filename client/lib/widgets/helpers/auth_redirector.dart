import 'package:flutter/material.dart';
import 'package:pisec_client/viewmodels/auth_state.dart';

class AuthRedirector extends StatefulWidget {
  final AuthState authState;
  final Widget child;

  const AuthRedirector({
    super.key,
    required this.authState,
    required this.child,
  });

  @override
  State<StatefulWidget> createState() => _AuthRedirectorState();
}

class _AuthRedirectorState extends State<AuthRedirector> {
  @override
  void initState() {
    super.initState();
    widget.authState.addListener(_onAuthStateChanged);
  }

  @override
  void dispose() {
    widget.authState.removeListener(_onAuthStateChanged);
    super.dispose();
  }

  void _onAuthStateChanged() {
    // Ensures the user is forced to login page if unauthenticated
    if (!widget.authState.isAuthenticated) {
      Navigator.of(context).pushNamedAndRemoveUntil("/login", (route) => false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return widget.child;
  }
}
