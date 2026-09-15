import 'package:shared_preferences/shared_preferences.dart';

class ServerConfigRepository {
  static const _keyServerUrl = "server_url";

  final Future<SharedPreferences> _prefFuture = SharedPreferences.getInstance();

  Future<String> getServerUrl() async {
    final pref = await _prefFuture;
    try {
      // If somehow a non-string is stored with key server_url, this will throw
      return pref.getString(_keyServerUrl) ?? "";
    } catch (e) {
      return "";
    }
  }

  Future<void> setServerUrl(String url) async {
    final pref = await _prefFuture;
    pref.setString(_keyServerUrl, url);
  }

  Future<void> clearServerUrl() async {
    final pref = await _prefFuture;
    pref.remove(_keyServerUrl);
  }
}
