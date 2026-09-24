import 'package:pisec_client/repositories/api/generic/user_repository.dart';

class ProfileRouteArgs {
  final UserRepository userRepository;
  final String initialEmail;

  const ProfileRouteArgs({
    required this.userRepository,
    this.initialEmail = "",
  });
}
