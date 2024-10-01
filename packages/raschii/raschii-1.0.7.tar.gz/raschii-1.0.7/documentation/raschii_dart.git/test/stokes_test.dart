import 'dart:math';
import "package:test/test.dart";
import '../raschii/stokes.dart';
import 'utils.dart';

void main() {
  test("Test case from the paper", () {
    double kd = 0.753982;
    double length = 100.0;
    double height = 1.0;
    double depth = kd * length / (2 * PI);
    var wave = new StokesWaves(height, depth, length, 5);

    Map<String, double> refvals = {
      'A11': 1.208490,
      'A22': 0.799840,
      'A31': -9.105340,
      'A33': 0.368275,
      'A42': -12.196150,
      'A44': 0.058723,
      'A51': 108.467921,
      'A53': -6.941756,
      'A55': -0.074979,
      'B22': 2.502414,
      'B31': -5.731666,
      'B42': -32.407508,
      'B44': 14.033758,
      'B53': -103.445042,
      'B55': 37.200027,
      'C0': 0.798448,
      'C2': 1.940215,
      'C4': -12.970403,
      'D2': -0.626215,
      'D4': 3.257104,
      'E2': 1.781926,
      'E4': -11.573657
    };

    refvals.forEach((String k, double v) {
      expect(((wave.data[k] - v) / v).abs(), lessThan(3e-5));
    });
  });

  test("Stokes test 12_200_100_5", () {
    double height = 12.0;
    double depth = 200.0;
    double length = 100.0;
    int order = 5;
    var wave = new StokesWaves(height, depth, length, order);

    var etas = wave.eta([0.0, length / 2]);
    var vel_crest = wave.velocity(0.0, etas[0]);
    var vel_trough = wave.velocity(length / 2, etas[1]);

    expect(etas[0], near(2.073e+02, 1e-1));
    expect(etas[1], near(1.953e+02, 1e-1));
    expect(vel_crest[0], near(7.440e+00, 1e-1));
    expect(vel_trough[0], near(-3.026e+00, 1e-1));

    wave.info();
  });
}
