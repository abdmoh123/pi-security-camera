extension ListExtensions<T> on List<T> {
  bool deepEquals(List<T> other) {
    if (length != other.length) return false;

    for (int i = 0; i < length; i++) {
      if (this[i] != other[i]) return false;
    }
    return true;
  }
}

extension NullableListExtensions<T> on List<T>? {
  bool nullabilityEquals(List<T>? other) {
    return (this == null) == (other == null);
  }
}
