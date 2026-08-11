import 'package:flutter/services.dart';

sealed class SecureStorageException implements Exception {
  final String message;
  final PlatformException? cause;
  final StackTrace? stackTrace;

  const SecureStorageException(this.message, {this.cause, this.stackTrace});

  @override
  String toString() => message;
}

sealed class ClearableSecureStorageException extends SecureStorageException {
  final FailedClearException? clearError;

  const ClearableSecureStorageException(
    super.message, {
    super.cause,
    super.stackTrace,
    this.clearError,
  });
}

class FailedClearException extends SecureStorageException {
  const FailedClearException(super.message, {super.cause, super.stackTrace});
}

class FailedReadException extends ClearableSecureStorageException {
  const FailedReadException(
    super.message, {
    super.cause,
    super.stackTrace,
    super.clearError,
  });
}

class FailedWriteException extends ClearableSecureStorageException {
  const FailedWriteException(
    super.message, {
    super.cause,
    super.stackTrace,
    super.clearError,
  });
}

