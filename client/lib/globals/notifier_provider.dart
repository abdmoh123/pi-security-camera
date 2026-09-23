import 'package:flutter/material.dart';
import 'package:pisec_client/exceptions/scope_exceptions.dart';

class NotifierProvider<T extends ChangeNotifier> extends StatefulWidget {
  const NotifierProvider({
    super.key,
    required this.notifier,
    required this.child,
  });

  final T notifier;
  final Widget child;

  static T of<T extends ChangeNotifier>(
    BuildContext context, {
    bool listen = true,
  }) {
    final scope = listen
        ? context.dependOnInheritedWidgetOfExactType<_NotifierScope<T>>()
        : context.getInheritedWidgetOfExactType<_NotifierScope<T>>();

    if (scope == null) {
      throw MissingScopeException("ProviderScope not found in context");
    }
    if (scope.notifier == null) {
      throw MissingScopeException("ProviderScope listener not found in scope");
    }
    return scope.notifier!;
  }

  @override
  State<NotifierProvider<T>> createState() => _NotifierProviderState<T>();
}

class _NotifierProviderState<T extends ChangeNotifier>
    extends State<NotifierProvider<T>> {
  @override
  void dispose() {
    widget.notifier.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return _NotifierScope<T>(notifier: widget.notifier, child: widget.child);
  }
}

class _NotifierScope<T extends ChangeNotifier> extends InheritedNotifier<T> {
  const _NotifierScope({
    super.key,
    required super.notifier,
    required super.child,
  });
}
