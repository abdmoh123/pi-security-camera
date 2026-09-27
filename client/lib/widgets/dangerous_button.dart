import 'package:flutter/material.dart';

enum ButtonType { filled, outline }

class DangerousButton extends StatelessWidget {
  final void Function()? onPressed;
  final Widget? child;
  final ButtonType _buttonType;

  const DangerousButton({
    super.key,
    required this.onPressed,
    required this.child,
    ButtonType buttonType = ButtonType.filled,
  }) : _buttonType = buttonType;

  factory DangerousButton.filled({void Function()? onPressed, Widget? child}) {
    return DangerousButton(
      onPressed: onPressed,
      buttonType: ButtonType.filled,
      child: child,
    );
  }

  factory DangerousButton.outline({void Function()? onPressed, Widget? child}) {
    return DangerousButton(
      onPressed: onPressed,
      buttonType: ButtonType.outline,
      child: child,
    );
  }

  @override
  Widget build(BuildContext context) {
    switch (_buttonType) {
      case ButtonType.filled:
        return FilledButton(
          onPressed: onPressed,
          style: FilledButton.styleFrom(
            backgroundColor: Theme.of(context).colorScheme.error,
            foregroundColor: Theme.of(context).colorScheme.onError,
          ),
          child: child,
        );
      case ButtonType.outline:
        return OutlinedButton(
          onPressed: onPressed,
          style: OutlinedButton.styleFrom(
            foregroundColor: Theme.of(context).colorScheme.error,
            side: BorderSide(color: Theme.of(context).colorScheme.error),
          ),
          child: child,
        );
    }
  }
}
