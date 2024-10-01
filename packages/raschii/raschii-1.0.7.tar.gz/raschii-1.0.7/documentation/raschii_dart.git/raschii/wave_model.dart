abstract class WaveModel {
  double length, height, depth;
  double k, omega, c;
  double g = 9.81;

  List<double> velocity(double x, double z);

  List<double> eta(List<double> x);
  String info() => '';
  String get_errors() => '';
  String get_warnings() => '';
}