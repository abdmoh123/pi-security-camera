class MissingScopeException implements Exception {
  final String message;

  const MissingScopeException(this.message);

  @override
  String toString() => message;
}
