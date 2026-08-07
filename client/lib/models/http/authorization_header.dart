import 'dart:io';

import 'package:pisec_client/models/http/http_header.dart';
import 'package:pisec_client/models/token.dart';
import 'package:pisec_client/types/token_type.dart';

class AuthorizationHeader implements HttpHeader {
  final String accessToken;
  final TokenType tokenType;

  const AuthorizationHeader(
    this.accessToken, {
    this.tokenType = TokenType.bearer,
  });

  AuthorizationHeader.fromToken(Token token)
    : this(token.accessToken, tokenType: token.tokenType);

  @override
  Map<String, String> toDict() => {
    HttpHeaders.authorizationHeader: "${tokenType.label} $accessToken",
  };
}
