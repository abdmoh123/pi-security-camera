import 'package:flutter/material.dart';
import 'package:pisec_client/exceptions/scope_exceptions.dart';
import 'package:pisec_client/viewmodels/auth_state.dart';

class AuthStateScope extends InheritedNotifier {
  const AuthStateScope({
    super.key,
    required AuthState authState,
    required super.child,
  }) : super(notifier: authState);

  static AuthState of(BuildContext context) {
    final scope = context.dependOnInheritedWidgetOfExactType<AuthStateScope>();
    if (scope == null) {
      throw MissingScopeException("AuthStateScope not found in context");
    }
    if (scope.notifier == null) {
      throw MissingScopeException("AuthStateScope listener not found in scope");
    }
    return scope.notifier! as AuthState;
  }
}
