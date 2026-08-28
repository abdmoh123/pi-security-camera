import 'package:pisec_client/models/json_serialisable.dart';
import 'package:pisec_client/types/token_type.dart';

class Token implements JsonSerialisable {
  final String accessToken;
  final String refreshToken;
  final TokenType tokenType;

  const Token({
    required this.accessToken,
    required this.refreshToken,
    this.tokenType = TokenType.bearer,
  });

  factory Token.fromJson(Map<String, dynamic> json) {
    return Token(
      accessToken: json['access_token'],
      refreshToken: json['refresh_token'],
      tokenType: TokenType.values.byName(json['token_type']),
    );
  }

  @override
  Map<String, dynamic> toJson() => {
    'access_token': accessToken,
    'refresh_token': refreshToken,
    'token_type': tokenType.name,
  };

  static bool validateJson(Map<String, dynamic> json) {
    return json.containsKey('access_token') &&
        json.containsKey('refresh_token') &&
        json.containsKey('token_type');
  }

  static Map<String, dynamic> generateJsonStruct() {
    final keys = Token(accessToken: '', refreshToken: '').toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }
}
