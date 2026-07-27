import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;
import 'package:pisec_client/models/token.dart';

class LoginAPIService {
  final http.Client client;
  final String baseUrl;

  const LoginAPIService(this.client, this.baseUrl);

  Future<bool> isReachable() async {
    final respose = await client.get(Uri.parse(baseUrl));
    return respose.statusCode == 200;
  }

  Future<Token> login(String username, String password) async {
    final response = await client.post(
      Uri.parse("$baseUrl/auth/token"),
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: {
        "username": username,
        "password": password,
        "grant_type": "password",
      },
    );

    if (response.statusCode != 200) {
      throw Exception('Error ${response.statusCode}: Failed to login');
    }
    return Token.fromJson(jsonDecode(response.body));
  }

  Future<void> logout(Token token) async {
    final response = await client.post(
      Uri.parse("$baseUrl/auth/logout"),
      headers: {HttpHeaders.authorizationHeader: "Bearer ${token.accessToken}"},
      body: {"refresh_token": token.refreshToken},
    );

    if (response.statusCode != 204) {
      throw Exception('Error ${response.statusCode}: Failed to logout');
    }
  }

  Future<void> logoutAll(String accessToken) async {
    final response = await client.post(
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
    final response = await client.post(
      Uri.parse("$baseUrl/auth/refresh"),
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      body: {"refresh_token": refreshTokenValue},
    );

    if (response.statusCode != 200) {
      throw Exception('Error ${response.statusCode}: Failed to refresh token');
    }
    return Token.fromJson(jsonDecode(response.body));
  }
}
