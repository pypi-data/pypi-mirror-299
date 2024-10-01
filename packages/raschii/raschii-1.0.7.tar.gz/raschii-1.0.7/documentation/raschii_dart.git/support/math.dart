import 'dart:math';

// -- Hyperbolic functions  ----------------------------------------------

// Hyperbolic functions are missing from the standard libraries
// IMPORTANT: there are better ways to implement these than the
// current straight from textbook definitions. Checking the sign
// of x is common in many implementations to avoid tending to inf
// in parts of the expressions etc.

double sinh(double x) => (exp(2 * x) - 1) / (2 * exp(x));
double cosh(double x) => (exp(2 * x) + 1) / (2 * exp(x));
double sech(double x) => (2 * exp(x) / (exp(2 * x) + 1));
double csch(double x) => (2 * exp(x) / (exp(2 * x) - 1));

double tanh(double x) {
  var a = exp(-2 * x);
  return (1 - a) / (1 + a);
}

double cotanh(double x) {
  var a = exp(-2 * x);
  return (1 + a) / (1 - a);
}

// -- Non standard hyperbolic functions ----------------------------------

/// A version of sinh(a)/cosh(b) where "b = a * f" and f is close to 1.
/// This can then be written exp(a * (1 - f)) for large a
double sinh_by_cosh(double a, double b) {
  if (a == 0) return 0.0;
  final double f = b / a;
  if ((a > 30 && 0.5 < f && f < 1.5) || (a > 200 && 0.1 < f && f < 1.9)) {
    return exp(a * (1 - f));
  }
  return sinh(a) / cosh(b);
}

/// A version of cosh(a)/cosh(b) where "b = a * f" and f is close to 1.
/// This can then be written exp(a * (1 - f)) for large a
double cosh_by_cosh(double a, double b) {
  if (a == 0) return sech(b);
  final double f = b / a;
  if ((a > 30 && 0.5 < f && f < 1.5) || (a > 200 && 0.1 < f && f < 1.9)) {
    return exp(a * (1 - f));
  }
  return cosh(a) / cosh(b);
}
