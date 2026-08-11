import 'dart:async';

import 'package:http/http.dart' as http;
import 'package:pisec_client/exceptions/http_exceptions.dart';
import 'package:pisec_client/exceptions/secure_storage_exceptions.dart';
import 'package:pisec_client/models/api/token.dart';
import 'package:pisec_client/repositories/token_repository.dart';
import 'package:pisec_client/services/login_api_service.dart';

class AuthHttpClient extends http.BaseClient {
  final http.Client _inner = http.Client();
  final TokenRepository tokenStorage;
  final LoginAPIService authService;

  bool _isRefreshing = false;
  final List<Completer<void>> _pendingRequests = [];

  AuthHttpClient(this.tokenStorage, this.authService);

  @override
  Future<http.StreamedResponse> send(http.BaseRequest request) async {
    final token = await tokenStorage.getToken();

    if (token != null) {
      request.headers['Authorization'] =
          '${token.tokenType.label} ${token.accessToken}';
    }

    final response = await _inner.send(request);

    if (response.statusCode == 401) {
      // Token might have been refreshed already by another call
      final currentToken = await tokenStorage.getToken();
      if (currentToken != null &&
          currentToken.accessToken != token?.accessToken) {
        return _inner.send(_cloneRequest(request, currentToken));
      }

      // Could fail when refreshing token or when saving it
      // If the token expires or if saving the token failed, then the token is
      // cleared automatically
      await _refreshTokenIfNeeded();

      final newToken = await tokenStorage.getToken();
      if (newToken == null) {
        throw FailedReadException(
          "Failed to read token after successful refresh",
        );
      }

      final newRequest = _cloneRequest(request, newToken);
      return _inner.send(newRequest);
    }

    return response;
  }

  @override
  void close() {
    _inner.close();
    super.close();
  }

  http.BaseRequest _cloneRequest(http.BaseRequest original, Token token) {
    late http.BaseRequest clone;
    switch (original) {
      case http.Request req:
        clone = http.Request(req.method, req.url)
          ..headers.addAll(req.headers)
          ..followRedirects = req.followRedirects
          ..maxRedirects = req.maxRedirects
          ..persistentConnection = req.persistentConnection
          ..encoding = req.encoding
          ..bodyBytes = req.bodyBytes;
        break;
      default:
        throw UnsupportedError(
          'Cloning not implemented for ${original.runtimeType}',
        );
    }

    clone.headers['Authorization'] =
        '${token.tokenType.label} ${token.accessToken}';

    return clone;
  }

  Future<void> _refreshTokenIfNeeded() async {
    if (_isRefreshing) {
      final completer = Completer<void>();
      _pendingRequests.add(completer);
      return completer.future;
    }
    _isRefreshing = true;

    try {
      final token = await tokenStorage.getToken();
      if (token == null) {
        throw FailedReadException('Failed to read token during refresh');
      }

      Token? newToken;
      try {
        newToken = await authService
            .refreshToken(token.refreshToken)
            .timeout(Duration(seconds: 10));
      } on HttpCodedException catch (e) {
        // Refresh token probably expired here, so stored token needs to be
        // cleared
        if (e.statusCode == 401) {
          await tokenStorage.clear();
        }
        rethrow;
      }

      // Could potentially fail (token would be cleared anyway)
      await tokenStorage.saveToken(newToken);

      for (final c in _pendingRequests) {
        c.complete();
      }
      _pendingRequests.clear();
    } catch (e, st) {
      for (final c in _pendingRequests) {
        c.completeError(e, st);
      }
      _pendingRequests.clear();

      rethrow;
    } finally {
      _isRefreshing = false;
    }
  }
}
