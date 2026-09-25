import 'package:pisec_client/repositories/api/generic/user_repository.dart';

class CredentialsRouteArgs {
  final UserRepository userRepository;

  const CredentialsRouteArgs({required this.userRepository});
}
