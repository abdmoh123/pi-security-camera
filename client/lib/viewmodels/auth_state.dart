import 'package:flutter/material.dart';
import 'package:pisec_client/exceptions/http_exceptions.dart';
import 'package:pisec_client/exceptions/secure_storage_exceptions.dart';
import 'package:pisec_client/models/api/queryables/user_query.dart';
import 'package:pisec_client/models/api/token.dart';
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

    final token = await _tokenRepository.getToken();
    if (token == null) {
      _isAuthenticated = false;
      _currentUser = null;
      if (oldIsAuthenticated != _isAuthenticated) {
        notifyListeners();
      }
      return;
    }

    // Make sure the auth service has the right baseUrl
    loginService.setBaseUrl(await _loginMemory.getServerUrl());
    // Make sure the current user has the right email/username
    _currentUser ??= UserQuery(email: await _loginMemory.getUsername());

    try {
      _isAuthenticated = await loginService.isRefreshTokenValid(
        token.refreshToken,
      );
    } on HttpCodedException {
      // We are not handling response mismatch exception, as it doesn't indicate
      // whether or not the refresh token has expired.
      // Better for the code to break quickly so we can fix it straight away
      // (it should never be thrown).
      _isAuthenticated = false;
      _currentUser = null;
      try {
        await _tokenRepository.clear();
      } on FailedClearException {
        // Nothing to do tbh
      }
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

    loginService.setBaseUrl(serverUrl);

    late final Token token;
    try {
      token = await loginService.login(userQuery);
    } on HttpCodedException {
      // End early as login has failed
      // Auth state hasn't changed, so no need to notify listeners
      return;
    } on ArgumentError {
      // End early as login has failed
      // Auth state hasn't changed, so no need to notify listeners
      return;
    }

    // Don't keep password in memory
    _currentUser = UserQuery(email: userQuery.email);

    await _loginMemory.setServerUrl(serverUrl);
    await _loginMemory.setUsername(_currentUser?.email ?? "");

    try {
      await _tokenRepository.saveToken(token);
    } on FailedWriteException {
      // Try to logout since we aren't able to store the token anyway
      try {
        await loginService.logout(token);
      } on HttpCodedException {
        // We failed to logout and failed to store the refresh token, which
        // means that a dangling unused refresh token will eventually exist on
        // the server
        // TODO: Add retry functionality
      }
      // End early as we aren't able to store the token and therefore do any
      // authourised communication with the server
      // No need to notify listeners as auth state hasn't changed
      return;
    }

    _isAuthenticated = true;

    notifyListeners();
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
      await loginService.logout(token);
    } on HttpCodedException {
      // End early as the logout failed
      // We don't need to notify listeners because the user is still
      // authenticated due to the logout failing
      // TODO: Have the logout service try to repeat the attempt if failed
      return;
    }
    _isAuthenticated = false;
    _currentUser = null;

    try {
      await _tokenRepository.clear();
    } on FailedClearException {
      // Failed to clear token, not sure what to do here
      // Keep in mind that this clear function has repeat tries built-in (3 by default)
      // If server didn't bug out and logout was cancelled, then nothing has changed
    }

    notifyListeners();
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
      // Get rid of old tokens and logout
      await loginService.logout(oldToken);
    } on HttpCodedException {
      // If logout failed, then the refresh token on server has already been
      // removed, so we don't need to do anything
    }

    _isAuthenticated = false;

    try {
      await _tokenRepository.clear();
    } on FailedClearException {
      // Not sure how to handle failed token clear
      // I guess we can ignore it for now as it can just be overwritten
    }

    late final Token newToken;
    try {
      // Update the token and stored user data
      newToken = await loginService.login(userQuery);
    } on HttpCodedException {
      // Login request was rejected
      // End early, we failed to login, so this function should act like a logout
      // TODO: Add retry functionality, just in case one request had bad luck
      notifyListeners();
      return;
    } on ArgumentError {
      // User input is missing email or password here (null values)
      // This should never happen in practice, as the UI should at least give
      // empty strings instead of null values
      // End early, we failed to login, so this function should act like a logout
      notifyListeners();
      return;
    }

    try {
      await _tokenRepository.saveToken(newToken);
    } on FailedWriteException {
      // If we get here, that means that the login was successful, but the device
      // couldn't save the refresh token in secure persistent storage (despite
      // the built-in repeat tries)
      try {
        await loginService.logout(newToken);
      } on HttpCodedException {
        // We failed to logout and failed to store the refresh token, which
        // means that a dangling unused refresh token will eventually exist on
        // the server
        // TODO: Add retry functionality
      }
      // End early as we aren't able to store the token and therefore do any
      // authourised communication with the server
      notifyListeners();
      return;
    }

    // We are considered authenticated if token was saved successfully
    _isAuthenticated = true;

    // Don't keep password in memory
    _currentUser = UserQuery(email: userQuery.email);
    await _loginMemory.setUsername(_currentUser?.email ?? "");

    notifyListeners();
  }
}
