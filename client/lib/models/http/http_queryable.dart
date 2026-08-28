abstract interface class PathQueryable {
  String toPathQueryString();

  static String combineToPathQueryString(Iterable<PathQueryable> queries) {
    return queries
        .where((q) => q.toPathQueryString().isNotEmpty)
        .map((q) => q.toPathQueryString())
        .join('&');
  }
}
