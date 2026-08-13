abstract interface class PathQueryable {
  String toPathQueryString();

  static String combineToPathQueryString(Iterable<PathQueryable> queries) {
    return queries.map((q) => q.toPathQueryString()).join('&');
  }
}
