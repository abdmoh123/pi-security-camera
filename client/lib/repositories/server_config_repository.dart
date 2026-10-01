import 'package:shared_preferences/shared_preferences.dart';

class LoginMemoryRepository {
  static const _serverUrlKey = "server_url";
  static const _usernameKey = "username";

  final Future<SharedPreferences> _prefFuture = SharedPreferences.getInstance();

  Future<String> getServerUrl() async {
    final pref = await _prefFuture;
    try {
      // If somehow a non-string is stored with key server_url, this will throw
      return pref.getString(_serverUrlKey) ?? "";
    } catch (e) {
      return "";
    }
  }

  Future<void> setServerUrl(String url) async {
    final pref = await _prefFuture;
    pref.setString(_serverUrlKey, url);
  }

  Future<void> clearServerUrl() async {
    final pref = await _prefFuture;
    pref.remove(_serverUrlKey);
  }

  Future<String> getUsername() async {
    final pref = await _prefFuture;
    try {
      // If somehow a non-string is stored, this will throw
      return pref.getString(_usernameKey) ?? "";
    } catch (e) {
      return "";
    }
  }

  Future<void> setUsername(String username) async {
    final pref = await _prefFuture;
    pref.setString(_usernameKey, username);
  }

  Future<void> clearUsername() async {
    final pref = await _prefFuture;
    pref.remove(_usernameKey);
  }
}
