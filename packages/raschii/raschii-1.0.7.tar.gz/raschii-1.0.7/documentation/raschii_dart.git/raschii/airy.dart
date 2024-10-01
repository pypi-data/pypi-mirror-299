import 'dart:math';
import '../support/math.dart';
import 'wave_model.dart';


class AiryWaves extends WaveModel {
  String warnings = '';

  AiryWaves(double height, double depth, double length, [int order=1]) {
    this.height = height;
    this.depth = depth;
    this.length = length;
    
    k = 2 * PI / length;
    omega = sqrt(k * g * tanh(k * depth));
    c = omega / k;

    if (order != 1) {
      warnings = 'Airy waves are linear, using order 1';
    }
  }

  List<double> eta(List<double> x) {
    var eta = new List<double>.from(x);
    for (var i = 0; i < x.length; i++) {
      eta[i] = depth + height / 2 * cos(x[i] * 2 * PI / length);
    }
    return eta;
  }

  List<double> velocity(double x, double z) {
    double ux = omega * height/ 2 * cosh(k * z) / sinh(k * depth) * cos(k * x);
    double uz = omega * height/ 2 * sinh(k * z) / sinh(k * depth) * sin(k * x);
    return [ux, uz];
  }

  String get_warnings() => warnings;
}