import 'package:flutter/services.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:pisec_client/models/token.dart';
import 'package:pisec_client/types/token_type.dart';

class TokenRepository {
  final _storage = const FlutterSecureStorage();

  Future<void> clear({int retryCount = 3}) async {
    try {
      await Future.wait([
        _storage.delete(key: "token_type"),
        _storage.delete(key: "access_token"),
        _storage.delete(key: "refresh_token"),
      ]);
    } on PlatformException {
      if (retryCount == 0) {
        rethrow;
      }
      await Future.delayed(Duration(milliseconds: 100));
      await clear(retryCount: retryCount - 1);
    }
  }

  Future<Token?> getToken({int retryCount = 3}) async {
    try {
      final (tokenTypeStr, accessToken, refreshToken) = await (
        _storage.read(key: "token_type"),
        _storage.read(key: "access_token"),
        _storage.read(key: "refresh_token"),
      ).wait;

      if (tokenTypeStr == null || accessToken == null || refreshToken == null) {
        return null;
      }

      return Token(
        accessToken: accessToken,
        refreshToken: refreshToken,
        tokenType: TokenType.fromName(tokenTypeStr),
      );
    } on PlatformException {
      if (retryCount == 0) {
        // Token is probably unrecoverable
        await clear();
        return null;
      }
      await Future.delayed(Duration(milliseconds: 100));
      return await getToken(retryCount: retryCount - 1);
    }
  }

  Future<void> saveToken(Token token, {int retryCount = 3}) async {
    try {
      await Future.wait([
        _storage.write(key: "token_type", value: token.tokenType.name),
        _storage.write(key: "access_token", value: token.accessToken),
        _storage.write(key: "refresh_token", value: token.refreshToken),
      ]);
    } on PlatformException {
      if (retryCount == 0) {
        // Ensure the token is not partially saved (either fully or not at all)
        await clear();
        rethrow;
      }
      await Future.delayed(Duration(milliseconds: 100));
      await saveToken(token, retryCount: retryCount - 1);
    }
  }
}
