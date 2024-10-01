import "package:test/test.dart";

Matcher near(double value, [double epsilon=3.0e-16]) {
  return new NearMatcher(value, epsilon);
}

class NearMatcher extends Matcher {
  final double value;
  final double epsilon;

  const NearMatcher(this.value, this.epsilon);

  @override
  bool matches(Object object, Map<dynamic, dynamic> matchState) {
    if (object is! double)
      return false;
    if (object == value)
      return true;
    final double test = object;
    return (test - value).abs() <= epsilon;
  }

  @override
  Description describe(Description dsc) => dsc.add('$value (±$epsilon)');
}