import 'package:flutter/material.dart';
import 'package:pisec_client/widgets/dangerous_button.dart';

Future<bool> showDeleteDialog(
  BuildContext context, {
  Widget? title,
  Widget? subtitle,
  required String textToDelete,
  String deleteButtonText = "Delete",
  required Future<void> Function() onSubmit,
}) async {
  final result = await showAdaptiveDialog(
    context: context,
    builder: (context) => DeleteSubmitDialog(
      title: title,
      subtitle: subtitle,
      textToDelete: textToDelete,
      deleteButtonText: deleteButtonText,
      onSubmit: onSubmit,
    ),
  );

  return result ?? false;
}

class DeleteSubmitDialog extends StatefulWidget {
  final Widget? title;
  final Widget? subtitle;
  final String textToDelete;
  final String deleteButtonText;
  final Future<void> Function() onSubmit;

  const DeleteSubmitDialog({
    super.key,
    this.title,
    this.subtitle,
    required this.textToDelete,
    this.deleteButtonText = "Delete",
    required this.onSubmit,
  });

  @override
  State<StatefulWidget> createState() => _DeleteSubmitDialogState();
}

class _DeleteSubmitDialogState extends State<DeleteSubmitDialog> {
  bool _isSubmitting = false;

  final confirmController = TextEditingController();

  Future<void> _submit(BuildContext context) async {
    if (_isSubmitting) return;

    setState(() => _isSubmitting = true);

    late final bool succeeded;
    try {
      await widget.onSubmit();
      succeeded = true;
    } catch (e) {
      succeeded = false;
    }

    if (!context.mounted) return;
    Navigator.of(context).pop(succeeded);
  }

  @override
  Widget build(BuildContext context) {
    const spacing = 12.0;

    return PopScope(
      canPop: !_isSubmitting,
      child: AlertDialog.adaptive(
        title: widget.title,
        content: Column(
          children: [
            widget.subtitle ?? Container(),
            widget.subtitle != null
                ? const SizedBox(height: spacing)
                : Container(),
            TextField(
              controller: confirmController,
              autofocus: true,
              decoration: InputDecoration(
                hintText: widget.textToDelete,
                border: const OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: spacing),
            Text.rich(
              TextSpan(
                children: [
                  const TextSpan(text: "Type in "),
                  TextSpan(
                    text: widget.textToDelete,
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: Theme.of(context).colorScheme.primary,
                    ),
                  ),
                  const TextSpan(text: " to activate the delete button"),
                ],
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: _isSubmitting
                ? null
                : () => Navigator.of(context).pop(false),
            child: const Text("Cancel"),
          ),
          ValueListenableBuilder(
            valueListenable: confirmController,
            builder: (context, value, child) {
              // Dangerous button should be red by default
              return DangerousButton.filled(
                onPressed: value.text == widget.textToDelete && !_isSubmitting
                    ? () async => await _submit(context)
                    : null,
                child: Builder(
                  builder: (context) {
                    // Get the correct size to set the progress indicator
                    final style = DefaultTextStyle.of(context).style;
                    final size = MediaQuery.textScalerOf(
                      context,
                    ).scale(style.fontSize ?? 14);

                    // Show a progress indicator while submitting the form
                    return _isSubmitting
                        ? SizedBox.square(
                            dimension: size,
                            child: const CircularProgressIndicator(
                              strokeWidth: 2,
                            ),
                          )
                        : Text(widget.deleteButtonText);
                  },
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}
