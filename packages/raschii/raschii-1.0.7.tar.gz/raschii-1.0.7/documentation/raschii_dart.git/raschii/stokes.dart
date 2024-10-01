import 'dart:math';
import 'wave_model.dart';
import '../support/math.dart';

/// This implementation of Stokes waves of 1st through 5th order is based on
/// "A Fifth‐Order Stokes Theory for Steady Waves" by John D. Fenton (1985)
class StokesWaves extends WaveModel {
  int order;
  Map<String, double> data = {};
  String errors = '';
  String warnings = '';

  StokesWaves(double height, double depth, double length, int order) {
    this.height = height;
    this.depth = depth;
    this.length = length;
    this.order = order;
    if (order < 1) {
      warnings += 'Stokes order must be at least 1, using order 1\n';
      this.order = 1;
    }
    else if (order > 5) {
      warnings += 'Stokes order only implemented up to 5, using order 5\n';
      this.order = 5;
    }
    if (length * 10 > depth)
      warnings += 'Depth is less than ten times wave length, ' + 
                  'Stokes theory should only be used for deep water waves!\n';
    compute_data();

    k = 2 * PI / length;
    double eps = k * height / 2;
    c = (data['C0'] + pow(eps, 2) * data['C2'] + pow(eps, 4) * data['C4']) * sqrt(g / k);
    omega = c * k;
  }

  void compute_data() {
    double k = 2 * PI / length;
    double kd = k * depth;
    if (kd > 300) {
      kd = 300.0;
      warnings += 'Using depth ${(kd / k).toStringAsFixed(2)} in some calculations to avoid overflow';
    }
    double S = sech(2 * kd);
    double Sh = sinh(kd);
    double Th = tanh(kd);
    double CTh = cotanh(kd);

    // Parameters are zero if not used in linear theory
    data['A11'] = csch(kd);
    data['A22'] = 0.0;
    data['A31'] = 0.0;
    data['A33'] = 0.0;
    data['A42'] = 0.0;
    data['A44'] = 0.0;
    data['A51'] = 0.0;
    data['A53'] = 0.0;
    data['A55'] = 0.0;
    data['B22'] = 0.0;
    data['B31'] = 0.0;
    data['B42'] = 0.0;
    data['B44'] = 0.0;
    data['B53'] = 0.0;
    data['B55'] = 0.0;
    data['C0'] = sqrt(Th);
    data['C2'] = 0.0;
    data['C4'] = 0.0;
    data['D2'] = 0.0;
    data['D4'] = 0.0;
    data['E2'] = 0.0;
    data['E4'] = 0.0;

    if (order == 1) return;

    // Define additional constants needed for second order Stokes waves
    data['A22'] = 3 * pow(S, 2) / (2 * pow(1 - S, 2));
    data['B22'] = CTh * (1 + 2 * S) / (2 * (1 - S));
    data['C2'] = sqrt(Th) * (2 + 7 * pow(S, 2)) / (4 * pow(1 - S, 2));
    data['D2'] = - sqrt(CTh) / 2;
    data['E2'] = Th * (2 + 2 * S + 5 * pow(S, 2)) / (4 * pow(1 - S, 2));

    if (order == 2) return;

    // Define additional constants needed for third order Stokes waves
    data['A31'] = (-4 - 20 * S + 10 * pow(S, 2) - 13 * pow(S, 3)) / (8 * Sh * pow(1 - S, 3));
    data['A33'] = (-2 * pow(S, 2) + 11 * pow(S, 3)) / (8 * Sh * pow(1 - S, 3));
    data['B31'] = -3 * (1 + 3 * S + 3 * pow(S, 2) + 2 * pow(S, 3)) / (8 * pow(1 - S, 3));

    if (order == 3) return;

    // Define additional constants needed for forth order Stokes waves
    data['A42'] = (12 * S - 14 * pow(S, 2) - 264 * pow(S, 3) - 45 * pow(S, 4) - 13 * pow(S, 5)) /
                  (24 * pow(1 - S, 5));
    data['A44'] = (10 * pow(S, 3) - 174 * pow(S, 4) + 291 * pow(S, 5) + 278 * pow(S, 6)) /
                  (48 * (3 + 2 * S) * pow(1 - S, 5));
    data['B42'] = CTh * (6 - 26 * S - 182 * pow(S, 2) - 204 * pow(S, 3) - 
                         25 * pow(S, 4) + 26 * pow(S, 5))/(6 * (3 + 2 * S)* pow(1 - S, 4));
    data['B44'] = CTh * (24 + 92 * S + 122 * pow(S, 2) + 66* pow(S, 3) + 
                         67 * pow(S, 4) + 34* pow(S, 5))/(24 * (3 + 2 * S) * pow(1 - S, 4));
    data['C4'] = sqrt(Th) * (4 + 32 * S - 116 * pow(S, 2) - 400 * pow(S, 3) - 71 * pow(S, 4) + 
                             146 * pow(S, 5)) / (32 * pow(1 - S, 5));
    data['D4'] = sqrt(CTh) * (2 + 4 * S + pow(S, 2) + 2 * pow(S, 3)) / (8 * pow(1 - S, 3));
    data['E4'] = Th * (8 + 12 * S - 152 * pow(S, 2) - 308 * pow(S, 3) - 42 * pow(S, 4) + 
                       77 * pow(S, 5)) / (32 * pow(1 - S, 5));

    if (order == 4) return;

    // Define additional constants needed for fift order Stokes waves
    data['A51'] = (-1184 + 32 * S + 13232 * pow(S, 2) + 21712 * pow(S, 3) + 20940 * pow(S, 4) + 
                   12554 * pow(S, 5) - 500 * pow(S, 6) - 3341 * pow(S, 7) - 670 * pow(S, 8)) /
                  (64 * Sh * (3 + 2 * S)* (4 + S) * pow(1 - S, 6));
    data['A53'] = (4 * S + 105 * pow(S, 2) + 198 * pow(S, 3) - 1376 * pow(S, 4) - 1302  * pow(S, 5) -
                   117 * pow(S, 6) + 58 * pow(S, 7)) / (32 * Sh * (3 + 2 * S) * pow(1 - S, 6));
    data['A55'] = (-6 * pow(S, 3) + 272 * pow(S, 4) - 1552 * pow(S, 5) + 852 * pow(S, 6) +
                   2029 * pow(S, 7) + 430 * pow(S, 8)) / (64 * Sh * (3 + 2 * S) * (4 + S) * pow(1 - S, 6));
    data['B53'] = 9 * (132 + 17 * S - 2216 * pow(S, 2) - 5897 * pow(S, 3) - 6292 * pow(S, 4) -
                       2687 * pow(S, 5) + 194 * pow(S, 6) + 467 * pow(S, 7) + 82 * pow(S, 8)) /
                      (128 * (3 + 2 * S) * (4 + S) * pow(1 - S, 6));
    data['B55'] = 5 * (300 + 1579 * S + 3176 * pow(S, 2) + 2949 * pow(S, 3) + 1188 * pow(S, 4) +
                       675 * pow(S, 5) + 1326 * pow(S, 6) + 827 * pow(S, 7) + 130 * pow(S, 8)) / 
                      (384 * (3 + 2 * S) * (4 + S) * pow(1 - S, 6));
  }

  List<double> eta(List<double> x) {
    var eta = new List<double>.from(x);
    double d = depth;
    double eps = k * height / 2;
    double kd = k * d;

    for (var i = 0; i < x.length; i++) {
      eta[i] = kd +
               eps * cos(k * x[i]) + 
               pow(eps, 2) * data['B22'] * cos(2 * k * x[i]) +
               pow(eps, 3) * data['B31'] * (cos(k * x[i]) - cos(3 * k * x[i])) +
               pow(eps, 4) * (data['B42'] * cos(2 * k * x[i]) + 
                              data['B44'] * cos(4 * k * x[i])) +
               pow(eps, 5) * (-(data['B53'] + data['B55']) * cos(k * x[i]) + 
                              data['B53'] * cos(3 * k * x[i]) +
                              data['B55'] * cos(5 * k * x[i]));
      eta[i] /= k;
    }
    return eta;
  }

  /// Particle velocities underneath the wave
  List<double> velocity(double x, double z) {
    double eps = k * height / 2;

    double my_cosh_cos(int i, int j) {
      String n = 'A$i$j';
      if (data[n] == 0.0)
        return 0.0;
      else
        return pow(eps, i) * data[n] * j * k * cosh(j * k * z) * cos(j * k * x);
    }

    double my_sinh_sin(int i, int j) {
      String n = 'A$i$j';
      if (data[n] == 0.0)
        return 0.0;
      else
        return pow(eps, i) * data[n] * j * k * sinh(j * k * z) * sin(j * k * x);
    }
    
    double ux = my_cosh_cos(1, 1) + my_cosh_cos(2, 2) + my_cosh_cos(3, 1) +
                my_cosh_cos(3, 3) + my_cosh_cos(4, 2) + my_cosh_cos(4, 4) +
                my_cosh_cos(5, 1) + my_cosh_cos(5, 3) + my_cosh_cos(5, 5);
    double uz = my_sinh_sin(1, 1) + my_sinh_sin(2, 2) + my_sinh_sin(3, 1) +
                my_sinh_sin(3, 3) + my_sinh_sin(4, 2) + my_sinh_sin(4, 4) +
                my_sinh_sin(5, 1) + my_sinh_sin(5, 3) + my_sinh_sin(5, 5);
    double C = data['C0'] * sqrt(g * pow(k, -3));
    return [C * ux, C * uz];
  }

  String info() {
    String info = 'kd:    ${2 * PI / length * depth}\n';
    data.forEach((k, v) {
      int n = int.parse(k[1]);
      if (n <= order)
        info += '$k:    ${v.toStringAsExponential(5)}\n';
    });
    return info;
  }

  String get_errors() => this.errors;
  String get_warnings() => this.warnings;
}