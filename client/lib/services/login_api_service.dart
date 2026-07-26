import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;
import 'package:pisec_client/models/token.dart';

class LoginAPIService {
  final String baseUrl;

  const LoginAPIService(this.baseUrl);

  Future<bool> isReachable() async {
    final respose = await http.get(Uri.parse("$baseUrl/auth/token"));
    return respose.statusCode == 200;
  }

  Future<Token> login(String username, String password) async {
    final response = await http.post(
      Uri.parse("$baseUrl/auth/token"),
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: {
        "username": username,
        "password": password,
        "grant_type": "password",
      },
    );

    if (response.statusCode == 200) {
      return Token.fromJson(jsonDecode(response.body));
    }
    throw Exception('Error ${response.statusCode}: Failed to login');
  }

  Future<void> logout(Token token) async {
    final response = await http.post(
      Uri.parse("$baseUrl/auth/logout"),
      headers: {HttpHeaders.authorizationHeader: "Bearer ${token.accessToken}"},
      body: {"refresh_token": token.refreshToken},
    );

    if (response.statusCode != 204) {
      throw Exception('Error ${response.statusCode}: Failed to logout');
    }
  }

  Future<void> logoutAll(String accessToken) async {
    final response = await http.post(
      Uri.parse("$baseUrl/auth/logout"),
      headers: {HttpHeaders.authorizationHeader: "Bearer $accessToken"},
    );

    if (response.statusCode != 204) {
      throw Exception(
        'Error ${response.statusCode}: Failed to logout from all devices',
      );
    }
  }

  Future<Token> refreshToken(String refreshTokenValue) async {
    final response = await http.post(
      Uri.parse("$baseUrl/auth/refresh"),
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: {"refresh_token": refreshTokenValue},
    );

    if (response.statusCode == 200) {
      return Token.fromJson(jsonDecode(response.body));
    }
    throw Exception('Error ${response.statusCode}: Failed to refresh token');
  }
}
