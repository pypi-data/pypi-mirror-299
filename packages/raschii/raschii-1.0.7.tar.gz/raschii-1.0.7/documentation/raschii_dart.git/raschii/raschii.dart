import 'dart:math';
import '../support/math.dart';
import 'wave_model.dart'; export 'wave_model.dart';
import 'airy.dart';
import 'fenton.dart';
import 'stokes.dart';


final String version = "1.0.0";


// The implemented wave models;
var waveModels = {'Airy': 'Airy waves',
                  'Fenton': 'Fenton stream function waves',
                  'Stokes': 'Stokes waves'};

/// Construct a wave model from user input
WaveModel constructWaveModel(String modelName, double height, double depth, double length, num N) {
  switch (modelName) {
    case 'Airy':
      return new AiryWaves(height, depth, length, N);
    case 'Fenton':
      return new FentonWaves(height, depth, length, N);
    case 'Stokes':
      return new StokesWaves(height, depth, length, N);
    default:
      throw new ArgumentError('Wave model $modelName does not exist');
  }
}


/**
Return two empty strings if everything is OK, else a string with
warnings about breaking criteria and a string with warnings about
being close to a breaking criterion
*/
List<String> check_breaking_criteria(double height, double depth, double length) {
  List<String> cnames = ['Length criterion', 'Depth criterion', 'Combined criterion'];
  double h1 = 0.14 * length;
  double h2 = 0.78 * depth;
  double h3 = 0.142 * tanh(2 * PI * depth / length) * length;
  List<double> hmaxes = [h1, h2, h3];

  String err = '';
  String warn = '';
  for (var i = 0; i < cnames.length; i++) {
    String cname = cnames[i];
    double hmax = hmaxes[i];
    String hmaxs = hmax.toStringAsPrecision(5);
    if (height > hmax)
      err += '$cname is exceeded, height $height > $hmaxs\n';
    else if (height > hmax * 0.9)
      warn += '$cname is close to exceeded, height $height = $hmaxs * ' +
              '${(height / hmax).toStringAsPrecision(3)}\n';
    }
    
    return [err, warn];
}