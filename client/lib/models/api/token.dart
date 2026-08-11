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
      accessToken: json['accessToken'],
      refreshToken: json['refreshToken'],
      tokenType: TokenType.values.byName(json['tokenType']),
    );
  }

  @override
  Map<String, dynamic> toJson() => {
    'access_token': accessToken,
    'refresh_token': refreshToken,
    'token_type': tokenType.name,
  };

  static bool validateJson(Map<String, dynamic> json) {
    return json.containsKey('accessToken') &&
        json.containsKey('refreshToken') &&
        json.containsKey('tokenType');
  }

  static Map<String, dynamic> generateJsonStruct() {
    final keys = Token(accessToken: '', refreshToken: '').toJson().keys;
    return JsonSerialisable.createFakeJson(keys);
  }
}
