enum TokenType {
  bearer;

  static TokenType fromName(String name) =>
      TokenType.values.firstWhere((e) => e.name == name);

  String get label {
    switch (this) {
      case TokenType.bearer:
        return 'Bearer';
    }
  }
}
