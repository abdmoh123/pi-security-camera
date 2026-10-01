import 'package:flutter/material.dart';
import 'package:pisec_client/exceptions/http_exceptions.dart';
import 'package:pisec_client/exceptions/secure_storage_exceptions.dart';
import 'package:pisec_client/models/api/queryables/user_query.dart';
import 'package:pisec_client/repositories/server_config_repository.dart';
import 'package:pisec_client/repositories/token_repository.dart';
import 'package:pisec_client/services/login_api_service.dart';

class AuthState extends ChangeNotifier {
  final LoginMemoryRepository _loginMemory;
  final TokenRepository _tokenRepository;

  final LoginAPIService loginService;

  UserQuery? _currentUser;

  // So initial assert would notify listeners if user wasn't logged in
  bool _isAuthenticated = true;

  AuthState(this._loginMemory, this._tokenRepository, this.loginService);

  String get serverUrl => loginService.baseUrl ?? "";
  UserQuery? get currentUser => _currentUser;

  bool get isAuthenticated => _isAuthenticated;

  Future<void> assertAuthenticated() async {
    final oldIsAuthenticated = _isAuthenticated;
    try {
      final token = await _tokenRepository.getToken();
      if (token == null) {
        _isAuthenticated = false;
        return;
      }

      // Make sure the auth service has the right baseUrl
      loginService.setBaseUrl(await _loginMemory.getServerUrl());

      _currentUser ??= UserQuery(email: await _loginMemory.getUsername());

      _isAuthenticated = await loginService.isRefreshTokenValid(
        token.refreshToken,
      );
    } catch (e) {
      _isAuthenticated = false;
    } finally {
      if (oldIsAuthenticated != _isAuthenticated) {
        notifyListeners();
      }
    }
  }

  Future<void> login(String serverUrl, UserQuery userQuery) async {
    if (_isAuthenticated) {
      // Nothing will change so no need to notify or try to login
      return;
    }

    try {
      loginService.setBaseUrl(serverUrl);

      final token = await loginService.login(userQuery);

      // Don't keep password in memory
      _currentUser = UserQuery(email: userQuery.email);

      await _loginMemory.setServerUrl(serverUrl);
      await _loginMemory.setUsername(_currentUser?.email ?? "");

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
    // Should never really happen:
    // Unlikely for cleared token and _isAuthenticated to be true
    final token = await _tokenRepository.getToken();
    if (token == null) {
      _isAuthenticated = false;
      _currentUser = null;

      notifyListeners();
      return;
    }

    try {
      _isAuthenticated = false;
      _currentUser = null;

      await loginService.logout(token);
      await _tokenRepository.clear();

      notifyListeners();
    } on HttpCodedException {
      // Failed to logout, not sure what to do here
      // If server didn't bug out and logout was cancelled, then nothing has changed
    } on FailedClearException {
      // Failed to clear token, not sure what to do here
      // If server didn't bug out and logout was cancelled, then nothing has changed
    }
  }

  Future<void> reLogin(UserQuery userQuery) async {
    if (!_isAuthenticated) {
      // You can't re-login if you're not logged in. Use the login method
      return;
    }

    // Should never really happen:
    // Unlikely for cleared token and _isAuthenticated to be true
    final oldToken = await _tokenRepository.getToken();
    if (oldToken == null) {
      _isAuthenticated = false;
      _currentUser = null;

      notifyListeners();
      return;
    }

    try {
      try {
        // Get rid of old tokens and logout
        await loginService.logout(oldToken);

        // Authentication state is false only if logout didn't fail
        _isAuthenticated = false;

        await _tokenRepository.clear();
      } on HttpCodedException {
        // If logout failed, then the refresh token on server has already been
        // removed, so we don't need to do anything
      }

      // Update the token and stored user data
      final newToken = await loginService.login(userQuery);
      await _tokenRepository.saveToken(newToken);

      // We are considered authenticated if token was saved successfully
      _isAuthenticated = true;

      // Don't keep password in memory
      _currentUser = UserQuery(email: userQuery.email);
      await _loginMemory.setUsername(_currentUser?.email ?? "");

      notifyListeners();
    } on HttpCodedException {
      // Do nothing as _isAuthenticated is already false if it failed to log
      // back in
    } on ArgumentError {
      // Do nothing as _isAuthenticated is already false if it failed to log
      // back in
    }
  }
}
