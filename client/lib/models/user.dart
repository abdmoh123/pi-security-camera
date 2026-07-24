class User {
  const User(this.id, this.email, {this.isAdmin = false});

  final int id;
  final String email;
  final bool isAdmin;
}
