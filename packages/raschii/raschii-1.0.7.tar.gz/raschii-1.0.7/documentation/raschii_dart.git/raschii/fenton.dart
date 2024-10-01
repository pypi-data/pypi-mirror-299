import 'dart:math';
import '../support/math.dart';
import '../support/linalg.dart' show Matrix, Vector, trapz;
import 'wave_model.dart';

class FentonConvergenceError implements Exception {
  String message;
  FentonConvergenceError(this.message);
  String toString() => message;
}

class FentonWaves extends WaveModel {
  String warnings = '';
  String errors = '';
  int order;
  double relax = 0.5;

  List<double> x_collocated, eta_collocated, B;
  double B0, R, Q;

  FentonWaves(double height, double depth, double length, int order) {
    this.height = height;
    this.depth = depth;
    this.length = length;
    this.order = order;
    FentonCoefficients data;
    try {
      data = fenton_coefficients(height, depth, length, order, g, relax);
    } on FentonConvergenceError catch (e) {
      errors = e.message;
      return;
    } on Exception catch (e) {
      errors = e.toString();
      return;
    }
    x_collocated = data.x.toList();
    eta_collocated = data.eta.toList();
    B0 = data.B0;
    B = data.B.toList();
    k = data.k;
    c = data.c;
    R = data.R;
    Q = data.Q;
    omega = k * c;
  }

  List<double> eta(List<double> x) {
    // Cosine series coefficients for the elevation
    final int N = eta_collocated.length - 1;
    var E = new Vector(N + 1);
    for (var i = 0; i < N + 1; i++) {
      var e2 = new Vector.fromList(eta_collocated);
      for (var j = 0; j < N + 1; j++) {
        e2[j] *= cos(i * j * PI / N);
      }
      E[i] = trapz(e2);
    }
    // Cosine transformation of the elevation
    var eta = new List<double>.from(x);
    for (var i = 0; i < eta.length; i++) {
      var e2 = E.copy();
      for (var j = 0; j < N + 1; j++) {
        e2[j] *= cos(j * k * x[i]);
      }
      eta[i] = 2 * trapz(e2) / N;
    }
    return eta;
  }

  List<double> velocity(double x, double z) {
    double ux = 0.0;
    double uz = 0.0;
    for (var j = 1; j < order + 1; j++) {
      ux += k *
          j *
          B[j - 1] *
          cos(j * k * x) *
          cosh_by_cosh(j * k * z, j * k * depth);
      uz += k *
          j *
          B[j - 1] *
          sin(j * k * x) *
          sinh_by_cosh(j * k * z, j * k * depth);
    }
    return [ux, uz];
  }

  String info() {
    String info = 'Collocation point data:\n\n';
    info += '           x          eta\n';
    for (var i = 0; i < order + 1; i++) {
      String xi = x_collocated[i].toStringAsExponential(5);
      String ei = eta_collocated[i].toStringAsExponential(5);
      info += '  $xi   $ei\n';
    }
    info += '\n';
    info += 'Other coefficients:\n\n';
    info += '  B0:    ${B0.toStringAsExponential(5)}\n';
    info += '  Q:     ${Q.toStringAsExponential(5)}\n';
    info += '  R:     ${R.toStringAsExponential(5)}\n';
    for (var i = 0; i < order; i++) {
      String n = (i + 1).toString().padLeft(2, '0');
      info += '  B$n:   ${B[i].toStringAsExponential(5)}\n';
    }
    return info;
  }

  String get_warnings() => warnings;
  String get_errors() => errors;
}

/// Input guess / storage of optimization results
class FentonCoefficients {
  Vector x;
  Vector B;
  Vector eta;
  double B0, Q, R, c, k;
  FentonCoefficients(final int N) {
    B = new Vector(N);
    eta = new Vector(N + 1);
  }
}

/// Find B, Q and R by Newton-Raphson following Rienecker and Fenton (1981)
///
/// Using relaxation can help in some difficult cases, try a value less than 1
/// to decrease convergence speed, but increase chances of converging.
FentonCoefficients fenton_coefficients(final double height, final double depth,
    final double length, final int N, final double g, final double relax,
    [final int maxIter = 500,
    final double tolerance = 1e-8,
    final int numSteps]) {
  // Non dimensionalised input
  final double H = height / depth;
  final double lambda = length / depth;
  final double k = 2 * PI / lambda;
  double c = sqrt(tanh(k) / k);
  final double D = 1.0;
  final int N_unknowns = 2 * (N + 1) + 2;

  /// Construct an initial guess for the unknowns (assume linear wave)
  FentonCoefficients initial_guess(double H) {
    var guess = new FentonCoefficients(N);
    guess.B0 = c;
    guess.B[0] = -H / (4 * c * k);
    for (var i = 0; i < N + 1; i++) {
      guess.eta[i] = 1 + H / 2 * cos(k * i / N);
    }
    guess.Q = c;
    guess.R = 1 + 0.5 * c * c;
    return guess;
  }

  /// Find B, Q and R by Newton iterations starting from the given initial
  /// guesses. According to Rienecker and Fenton (1981) a linear theory
  /// initial guess should work unless H close to breaking, then an initial
  /// guess from the optimization routine run with a slightly lower H should
  /// be used instead.
  FentonCoefficients optimize(FentonCoefficients guess, double H) {
    // Insert initial guesses into coefficient vector
    var coeffs = new Vector(N_unknowns);
    for (var i = 0; i < N; i++) {
      coeffs[i + 1] = guess.B[i];
      coeffs[i + 1 + N] = guess.eta[i];
    }
    coeffs[0] = guess.B0;
    coeffs[2 * N + 1] = guess.eta[N];
    coeffs[2 * N + 2] = guess.Q;
    coeffs[2 * N + 3] = guess.R;

    int it;
    double error;
    var f = func(coeffs, H, k, D, N);
    for (it = 0; it < maxIter + 1; it++) {
      // Compute the coefficient increment
      final jac = fprime(coeffs, H, k, D, N);
      var delta = jac.solve_lup(f); // Should be -f, but see next line
      coeffs.axpy(-relax, delta); // Compensate for sign here
      f = func(coeffs, H, k, D, N);

      // Check the progress
      error = f.abs_max();
      double eta_min = double.INFINITY;
      double eta_max = double.NEGATIVE_INFINITY;
      for (var i = 0; i < N + 1; i++) {
        eta_min = min(coeffs[N + 1 + i], eta_min);
        eta_max = max(coeffs[N + 1 + i], eta_max);
      }
      if (eta_max > 2)
        throw new FentonConvergenceError('Optimization did not converge. Got '
            'max(eta)/depth = $eta_max in iteration $it');
      if (eta_min < 0.1)
        throw new FentonConvergenceError('Optimization did not converge. Got '
            'min(eta)/depth = $eta_min in iteration $it');
      if (error < tolerance) {
        var res = new FentonCoefficients(N);
        for (var i = 0; i < N; i++) {
          res.B[i] = coeffs[i + 1];
          res.eta[i] = coeffs[N + 1 + i];
        }
        res.B0 = coeffs[0];
        res.eta[N] = coeffs[2 * N + 1];
        res.Q = coeffs[2 * N + 2];
        res.R = coeffs[2 * N + 3];
        return res;
      }
    }
    throw new FentonConvergenceError('Optimization did not converge after'
        ' $it iterations, error = $error');
  }

  // Perform the optimization, optionally in steps gradually increasing H
  Vector steps = waveHeightSteps(numSteps, D, lambda, H);
  FentonCoefficients guess = initial_guess(steps[0]);
  for (double Hi in steps.toList()) {
    guess = optimize(guess, Hi);
  }

  // Collocation points
  var x = new Vector.arange(N + 1);
  x.scale(length / (2 * N));

  // Scale back to physical space
  guess.x = x;
  guess.B0 *= sqrt(g * depth);
  guess.B.scale(sqrt(g * depth * depth * depth));
  guess.eta.scale(depth);
  guess.Q *= sqrt(g * depth * depth * depth);
  guess.R *= g * depth;
  guess.c = guess.B0;
  guess.k = k / depth;
  return guess;
}

/// Compute the breaking height and use this to select how many steps to
/// take when gradually increasing the wave height to improve convergence
/// for high waves
Vector waveHeightSteps(int numSteps, double D, double lambda, double H) {
  // Breaking height
  double Hb = 0.142 * tanh(2 * PI * D / lambda) * lambda;

  // Try with progressively higher waves to get better initial conditions
  if (numSteps == null) {
    if (H > 0.75 * Hb)
      numSteps = 10;
    else if (H > 0.65 * Hb)
      numSteps = 5;
    else
      numSteps = 3;
  }
  if (numSteps == 1)
    return new Vector.fromList([H]);
  else
    return new Vector.linspace(H / numSteps, H, numSteps);
}

// -- Function -----------------------------------------------------------

/// The function to minimize
Vector func(final Vector coeffs, final double H, final double k, final double D,
    final int N) {
  final int N_unknowns = coeffs.size;

  final double B0 = coeffs[0];
  final B = coeffs.view(1, N + 1);
  final eta = coeffs.view(N + 1, 2 * N + 2);
  final double Q = coeffs[2 * N + 2];
  final double R = coeffs[2 * N + 3];

  // The function to be minimized
  var f = new Vector(N_unknowns);

  // Loop over the N + 1 points along the half wave
  for (var m = 0; m < N + 1; m++) {
    // Stream function at this location, static part
    // The sign of B0 is swapped from what is in the paper
    f[m] = -B0 * eta[m] + Q;

    // Velocities at this location, static part
    double um = -B0;
    double vm = 0.0;

    for (var j = 1; j < N + 1; j++) {
      final double S1 = sinh_by_cosh(j * k * eta[m], j * k * D);
      final double C1 = cosh_by_cosh(j * k * eta[m], j * k * D);
      final double S2 = sin(j * m * PI / N);
      final double C2 = cos(j * m * PI / N);

      // Enforce a streamline along the free surface
      f[m] += B[j - 1] * S1 * C2;

      // Velocity at the free surface
      // The sign of B0 is swapped from what is in the paper
      um += k * j * B[j - 1] * C1 * C2;
      vm += k * j * B[j - 1] * S1 * S2;
    }

    // Enforce the dynamic free surface boundary condition
    f[N + 1 + m] += (um * um + vm * vm) / 2 + eta[m] - R;
  }
  // Enforce mean(eta) = D
  f[2 * N + 2] = trapz(eta) / N - 1;

  // Enforce eta_0 - eta_N = H, the wave height criterion
  f[2 * N + 3] = eta[0] - eta[N] - H;
  return f;
}
// -- Jacobian -----------------------------------------------------------

/// The Jacobian of the function to minimize (numerical version)
Matrix fprime_num(final Vector coeffs, final double H, final double k,
    final double D, final int N) {
  final int Nc = coeffs.size;
  var jac = new Matrix(Nc, Nc);
  final double dc = 1e-10;
  final f0 = func(coeffs, H, k, D, N);

  var c2 = coeffs.copy();
  for (var i = 0; i < Nc; i++) {
    c2[i] = coeffs[i] + dc;
    c2[(i - 1) % Nc] = coeffs[(i - 1) % Nc];
    final f1 = func(c2, H, k, D, N);
    for (var j = 0; j < Nc; j++) {
      jac.set(j, i, (f1[j] - f0[j]) / dc);
    }
  }

  return jac;
}

/// The Jacobian of the function to minimize (analytical version)
Matrix fprime(final Vector coeffs, final double H, final double k,
    final double D, final int N) {
  final int Nc = coeffs.size;
  var jac = new Matrix(Nc, Nc);

  final double B0 = coeffs[0];
  final B = coeffs.view(1, N + 1);
  final eta = coeffs.view(N + 1, 2 * N + 2);

  for (var m = 0; m < N + 1; m++) {
    int m2 = m + N + 1;

    // Compute the velocity at this collocation point
    double um = -B0;
    double vm = 0.0;
    for (var j = 1; j < N + 1; j++) {
      final double S1 = sinh_by_cosh(j * k * eta[m], j * k * D);
      final double C1 = cosh_by_cosh(j * k * eta[m], j * k * D);
      final double S2 = sin(j * m * PI / N);
      final double C2 = cos(j * m * PI / N);

      // Velocity at the free surface
      um += k * j * B[j - 1] * C1 * C2;
      vm += k * j * B[j - 1] * S1 * S2;
    }

    for (var j = 1; j < N + 1; j++) {
      final double S1 = sinh_by_cosh(j * k * eta[m], j * k * D);
      final double C1 = cosh_by_cosh(j * k * eta[m], j * k * D);
      final double S2 = sin(j * m * PI / N);
      final double C2 = cos(j * m * PI / N);
      final double SC = S1 * C2;
      final double SS = S1 * S2;
      final double CC = C1 * C2;
      final double CS = C1 * S2;

      // Derivatives of the dynamic free surface boundary condition
      jac.set(m2, j, k * um * j * CC + k * vm * j * SS);
      double tmp = k * k * B[j - 1] * j * j;
      jac.add(m2, m2, um * tmp * SC + vm * tmp * CS);

      // Derivatives of the eq. for the streamline along the free surface
      jac.set(m, j, SC);
    }

    // Derivatives of the eq. for the streamline along the free surface
    jac.set(m, m2, um);
    jac.set(m, 0, -eta[m]);
    jac.set(m, Nc - 2, 1.0);

    // Derivatives of the dynamic free surface boundary condition
    jac.add(m2, m2, 1.0);
    jac.set(m2, Nc - 1, -1.0);
    jac.set(m2, 0, -um);

    // Derivative of mean(eta) = 1
    jac.set(Nc - 2, m2, 1 / N);
  }

  // Derivative of mean(eta) = 1
  jac.set(Nc - 2, N + 1, 1 / (2 * N));
  jac.set(Nc - 2, 2 * N + 1, 1 / (2 * N));

  // Derivative of the wave height criterion
  jac.set(Nc - 1, N + 1, 1.0);
  jac.set(Nc - 1, 2 * N + 1, -1.0);

  return jac;
}
