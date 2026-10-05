enum SortDirection {
  ascending,
  descending;

  String get queryString {
    switch (this) {
      case SortDirection.ascending:
        return "asc";
      case SortDirection.descending:
        return "desc";
    }
  }
}
