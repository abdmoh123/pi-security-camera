import 'package:pisec_client/services/login_api_service.dart';

class RegisterRouteArgs {
  final LoginAPIService authService;
  final String serverUrl;
  final String email;
  final void Function(String serverUrl, String email)? onSubmitSuccess;

  const RegisterRouteArgs({
    required this.authService,
    this.serverUrl = "",
    this.email = "",
    Function(String serverUrl, String email)? this.onSubmitSuccess,
  });
}
