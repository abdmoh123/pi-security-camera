abstract interface class HttpHeader {
  Map<String, String> toDict();

  static Map<String, String> combineToDict(Iterable<HttpHeader> headers) => {
    for (final header in headers) ...header.toDict(),
  };
}
