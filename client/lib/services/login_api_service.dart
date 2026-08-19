import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:pisec_client/constants/http/content_type_headers.dart';
import 'package:pisec_client/exceptions/http_exceptions.dart';
import 'package:pisec_client/extensions/http.dart';
import 'package:pisec_client/models/api/queryables/user_query.dart';
import 'package:pisec_client/models/api/responses/user_response.dart';
import 'package:pisec_client/models/api/token.dart';
import 'package:pisec_client/models/http/authorization_header.dart';
import 'package:pisec_client/types/token_type.dart';

class LoginAPIService {
  final http.Client client;
  final String baseUrl;

  const LoginAPIService(this.baseUrl, this.client);

  Future<bool> isReachable() async {
    final response = await client.get(Uri.parse(baseUrl));
    return response.ok;
  }

  Future<UserResponse> registerUser(UserQuery userQuery) async {
    // API expects both email and password
    ArgumentError.checkNotNull(userQuery.email, "userQuery.email");
    ArgumentError.checkNotNull(userQuery.password, "userQuery.password");

    final response = await client.post(
      Uri(path: "$baseUrl/users/"),
      body: userQuery.toJson(),
    );
    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: "Failed to register user",
      );
    }
    return UserResponse.fromJson(json.decode(response.body));
  }

  Future<Token> login(UserQuery userQuery) async {
    // API expects both email (username) and password
    ArgumentError.checkNotNull(userQuery.email, "userQuery.email");
    ArgumentError.checkNotNull(userQuery.password, "userQuery.password");

    final response = await client.post(
      Uri.parse("$baseUrl/auth/token"),
      headers: xWwwFormUrlencodedHeader.toDict(),
      body: {
        "username": userQuery.email,
        "password": userQuery.password,
        "grant_type": "password",
      },
    );

    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: 'Failed to login',
      );
    }

    final json = jsonDecode(response.body);
    if (!Token.validateJson(json)) {
      throw ResponseMismatchException(Token.generateJsonStruct(), json);
    }
    return Token.fromJson(json);
  }

  Future<void> logout(Token token) async {
    final response = await client.post(
      Uri.parse("$baseUrl/auth/logout"),
      headers: AuthorizationHeader.fromToken(token).toDict(),
      body: {"refresh_token": token.refreshToken},
    );

    if (response.statusCode != 204) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: 'Failed to logout',
      );
    }
  }

  Future<void> logoutAll(String accessToken) async {
    final response = await client.post(
      Uri.parse("$baseUrl/auth/logout"),
      headers: AuthorizationHeader(
        accessToken,
        tokenType: TokenType.bearer,
      ).toDict(),
    );

    if (response.statusCode != 204) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: 'Failed to logout from all devices',
      );
    }
  }

  Future<Token> refreshToken(String refreshTokenValue) async {
    final response = await client.post(
      Uri.parse("$baseUrl/auth/refresh"),
      headers: xWwwFormUrlencodedHeader.toDict(),
      body: {"refresh_token": refreshTokenValue},
    );

    if (response.notOk) {
      throw HttpCodedException(
        statusCode: response.statusCode,
        message: 'Failed to refresh token',
      );
    }

    final json = jsonDecode(response.body);
    if (!Token.validateJson(json)) {
      throw ResponseMismatchException(Token.generateJsonStruct(), json);
    }
    return Token.fromJson(json);
  }
}
