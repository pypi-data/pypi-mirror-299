import 'dart:math';
import "package:test/test.dart";
import '../raschii/fenton.dart';
import '../support/linalg.dart';
import 'utils.dart';

void main() {
  test("Test Fenton Jacobian", () {
    double height = 0.2;
    double depth = 1.0;
    double k = 1.5707963267948966;
    int order = 10;
    var coeffs = new Vector.fromList([
      -0.7641186499221805,
      -0.04165712827663715,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      0.0,
      1.1,
      1.0951056516295155,
      1.0809016994374947,
      1.0587785252292474,
      1.0309016994374947,
      1.0,
      0.9690983005625052,
      0.9412214747707527,
      0.9190983005625053,
      0.9048943483704847,
      0.9,
      0.7641186499221805,
      1.2919386555794479
    ]);

    var fpn = fprime_num(coeffs, height, k, depth, order);
    var fpa = fprime(coeffs, height, k, depth, order);

    expect(fpn.N, equals(fpa.N));
    expect(fpn.M, equals(fpa.M));
    for (var i = 0; i < fpn.N; i++) {
      for (var j = 0; j < fpn.M; j++) {
        //print('$i, $j, ${fpn.get(i,j)}, ${fpa.get(i,j)}');
        expect(fpa.get(i, j), near(fpn.get(i, j), 1e-5));
      }
    }
  });

  test("Fenton test 12_200_100_5", () {
    double height = 12.0;
    double depth = 200.0;
    double length = 100.0;
    int order = 5;
    var wave = new FentonWaves(height, depth, length, order);

    var etas = wave.eta([0.0, length / 2]);
    var vel_crest = wave.velocity(0.0, etas[0]);
    var vel_trough = wave.velocity(length / 2, etas[1]);

    expect(etas[0], near(2.074e+02, 1e-1));
    expect(etas[1], near(1.954e+02, 1e-1));
    expect(vel_crest[0], near(7.608e+00, 1e-1));
    expect(vel_trough[0], near(-2.992e+00, 1e-1));

    wave.info();
  });

  /// Compare with results obtained by
  /// https://github.com/roenby/fentonWave/blob/master/tests/fenton.m
  test("fenton_m_01", () {
    double height = 0.2;
    double depth = 0.5;
    double length = 2.0;
    int order = 30;
    var wave = new FentonWaves(height, depth, length, order);

    List<double> ml_eta = [
      6.256332118992537e-01,
      6.235402803532166e-01,
      6.176398294183506e-01,
      6.088383657880129e-01,
      5.981433292625251e-01,
      5.863925484803192e-01,
      5.741905043147202e-01,
      5.619444604418909e-01,
      5.499201111324211e-01,
      5.382877714262410e-01,
      5.271547620101914e-01,
      5.165868059915903e-01,
      5.066219276102671e-01,
      4.972795106660977e-01,
      4.885662821396637e-01,
      4.804803408120494e-01,
      4.730139306009313e-01,
      4.661553962008353e-01,
      4.598905967179053e-01,
      4.542039528250898e-01,
      4.490792405884328e-01,
      4.445002058220727e-01,
      4.404510478467331e-01,
      4.369168054556746e-01,
      4.338836674511877e-01,
      4.313392232541929e-01,
      4.292726644934076e-01,
      4.276749454052453e-01,
      4.265389076728026e-01,
      4.258593738023461e-01,
      4.256332118992525e-01
    ];
    List<double> ml_x = [
      0.000000000000000e+00,
      3.333333333333333e-02,
      6.666666666666667e-02,
      1.000000000000000e-01,
      1.333333333333333e-01,
      1.666666666666667e-01,
      2.000000000000000e-01,
      2.333333333333333e-01,
      2.666666666666667e-01,
      3.000000000000000e-01,
      3.333333333333333e-01,
      3.666666666666666e-01,
      4.000000000000000e-01,
      4.333333333333334e-01,
      4.666666666666667e-01,
      5.000000000000000e-01,
      5.333333333333333e-01,
      5.666666666666667e-01,
      6.000000000000000e-01,
      6.333333333333333e-01,
      6.666666666666666e-01,
      7.000000000000000e-01,
      7.333333333333333e-01,
      7.666666666666667e-01,
      8.000000000000000e-01,
      8.333333333333334e-01,
      8.666666666666668e-01,
      9.000000000000000e-01,
      9.333333333333333e-01,
      9.666666666666667e-01,
      1.000000000000000e+00
    ];
    List<double> ml_B = [
      2.882335299753824e-01,
      1.908361026480882e-02,
      8.213767815747559e-04,
      1.313097979767291e-04,
      3.462697008046542e-05,
      6.111647882537242e-06,
      1.086244274356666e-06,
      2.348957533655237e-07,
      5.188765616282414e-08,
      1.118382204680194e-08,
      2.478538275444786e-09,
      5.663408583688279e-10,
      1.314393502678408e-10,
      3.145814127549186e-11,
      8.003417970111735e-12,
      3.322723890828176e-12,
      3.846369798481719e-13,
      1.962769427566047e-12,
      -4.233208440136547e-13,
      1.977390134075710e-12,
      -1.407633578386493e-12,
      2.704910823483152e-12,
      -1.465002188938580e-12,
      1.163053015764832e-12,
      8.764635112300480e-13,
      -1.550809821892457e-12,
      3.324853049346685e-12,
      -3.355716762751551e-12,
      4.576015189520344e-12,
      -2.400972953139157e-12
    ];
    double ml_B0 = 1.799024665755609e+00;
    double ml_Q = 0.873795415021738;
    double ml_R = 6.53355446469293;
    double ml_k = 3.14159265358979;
    double ml_c = ml_B0;

    expect(wave.c, near(ml_c, 1e-7));
    expect(wave.k, near(ml_k, 1e-7));
    expect(wave.Q, near(ml_Q, 1e-7));
    expect(wave.R, near(ml_R, 1e-7));
    expect(wave.B0, near(ml_B0, 1e-7));

    expect(wave.x_collocated.length, equals(order + 1));
    expect(wave.eta_collocated.length, equals(order + 1));
    for (var i = 0; i < order + 1; i++) {
      expect(wave.x_collocated[i], near(ml_x[i]));
      expect(wave.eta_collocated[i], near(ml_eta[i], 1e-7));
    }

    expect(wave.B.length, equals(order));
    for (var i = 0; i < order; i++) {
      expect(wave.B[i], near(ml_B[i] * sqrt(9.81 / pow(ml_k, 3)), 1e-7));
    }
  });
}
