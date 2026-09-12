import 'package:flutter/material.dart';
import 'package:pisec_client/exceptions/http_exceptions.dart';
import 'package:pisec_client/exceptions/secure_storage_exceptions.dart';
import 'package:pisec_client/models/api/queryables/user_query.dart';
import 'package:pisec_client/repositories/token_repository.dart';
import 'package:pisec_client/services/login_api_service.dart';

class AuthState extends ChangeNotifier {
  final TokenRepository _tokenRepository;
  final LoginAPIService _authService;

  bool _isAuthenticated = false;

  AuthState(TokenRepository tokenRepository, LoginAPIService authService)
    : _tokenRepository = tokenRepository,
      _authService = authService;

  bool get isAuthenticated => _isAuthenticated;

  Future<void> assertAuthenticated() async {
    final oldIsAuthenticated = _isAuthenticated;
    try {
      final token = await _tokenRepository.getToken();
      if (token == null) {
        _isAuthenticated = false;
        return;
      }
      _isAuthenticated = await _authService.isRefreshTokenValid(
        token.refreshToken,
      );
    } on FailedReadException {
      _isAuthenticated = false;
    } on HttpCodedException {
      _isAuthenticated = false;
    } on ResponseMismatchException {
      _isAuthenticated = false;
    } finally {
      if (oldIsAuthenticated != _isAuthenticated) {
        notifyListeners();
      }
    }
  }

  Future<void> login(UserQuery userQuery) async {
    if (_isAuthenticated) {
      // Nothing will change so no need to notify or try to login
      return;
    }

    try {
      final token = await _authService.login(userQuery);
      await _tokenRepository.saveToken(token);
      _isAuthenticated = true;
      notifyListeners();
    } on HttpCodedException {
      // Do nothing as _isAuthenticated is already false
    } on ArgumentError {
      // Do nothing as _isAuthenticated is already false
    }
  }

  Future<void> logout() async {
    if (!_isAuthenticated) {
      // Nothing will change so no need to notify or try to logout
      return;
    }

    // Should never really happen:
    // Unlikely for cleared token and _isAuthenticated to be true
    final token = await _tokenRepository.getToken();
    if (token == null) {
      _isAuthenticated = false;
      notifyListeners();
      return;
    }

    try {
      await _authService.logout(token);
      await _tokenRepository.clear();
      _isAuthenticated = false;
      notifyListeners();
    } on HttpCodedException {
      // Failed to logout, not sure what to do here
      // If server didn't bug out and logout was cancelled, then nothing has changed
    } on FailedClearException {
      // Failed to clear token, not sure what to do here
      // If server didn't bug out and logout was cancelled, then nothing has changed
    }
  }
}
