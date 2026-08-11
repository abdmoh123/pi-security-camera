abstract interface class HttpQueryable {
  String toHttpQueryString();

  static String combineToHttpQueryString(Iterable<HttpQueryable> queries) {
    return queries.map((q) => q.toHttpQueryString()).join('&');
  }
}
