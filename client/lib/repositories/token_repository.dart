import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:pisec_client/models/token.dart';
import 'package:pisec_client/types/token_type.dart';

class TokenRepository {
  final _storage = const FlutterSecureStorage();

  Future<void> clear() async {
    await Future.wait([
      _storage.delete(key: "token_type"),
      _storage.delete(key: "access_token"),
      _storage.delete(key: "refresh_token"),
    ]);
  }

  Future<Token?> getToken() async {
    try {
      final (tokenTypeStr, accessToken, refreshToken) = await (
        _storage.read(key: "token_type"),
        _storage.read(key: "access_token"),
        _storage.read(key: "refresh_token"),
      ).wait;

      if (tokenTypeStr == null || accessToken == null || refreshToken == null) {
        throw Exception("Failed to read token from secure storage");
      }

      return Token(
        accessToken: accessToken,
        refreshToken: refreshToken,
        tokenType: TokenType.fromName(tokenTypeStr),
      );
    } catch (e) {
      return null;
    }
  }

  Future<void> saveToken(Token token) async {
    try {
      await Future.wait([
        _storage.write(key: "token_type", value: token.tokenType.name),
        _storage.write(key: "access_token", value: token.accessToken),
        _storage.write(key: "refresh_token", value: token.refreshToken),
      ]);
    } catch (e) {
      // Ensure the token is not partially saved (either fully or not at all)
      clear();
      rethrow;
    }
  }
}
