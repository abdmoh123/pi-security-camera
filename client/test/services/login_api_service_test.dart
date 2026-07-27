import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:pisec_client/services/login_api_service.dart';

import 'login_api_service_test.mocks.dart';

@GenerateMocks([], customMocks: [MockSpec<http.Client>(as: #MockHttpClient)])
void main() {
  test('Fake server should be reachable', () async {
    final mockClient = MockHttpClient();
    final baseUrl = 'http://localhost:8080';
    final loginAPIService = LoginAPIService(mockClient, baseUrl);

    when(
      mockClient.get(Uri.parse(baseUrl)),
    ).thenAnswer((_) async => http.Response('', 200));

    expect(await loginAPIService.isReachable(), isTrue);
  });
}
