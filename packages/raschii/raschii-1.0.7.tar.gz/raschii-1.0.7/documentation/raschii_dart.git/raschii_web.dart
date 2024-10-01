import 'dart:html';
import 'dart:svg';
import 'dart:math';
import 'raschii/raschii.dart';
import 'support/plotter.dart';


final String defaultModel = 'Stokes';


class RaschiiWeb {
  SelectElement modelElem;
  Element errorElem;
  Element warningElem;
  Element infoElem;
  Element plotElem;
  InputElement heightElem;
  InputElement depthElem;
  InputElement lengthElem;
  InputElement orderElem;
  OutputElement outputElem;
  ButtonElement generateElem;
  WaveModel wave;
  bool inputOk = false;

  RaschiiWeb(Element main) {
    // Add the available wave models to the drop down menu
    modelElem = main.querySelector('select[name="waveModel"]');
    waveModels.forEach((modelName, modelDescription) {
      var opt = new OptionElement(value: modelName,
                                  selected: modelName == defaultModel);
      opt.text = modelDescription;
      modelElem.children.add(opt);
    });

    // Remove the initial warnings
    errorElem = main.querySelector('.error');
    warningElem = main.querySelector('.warning');
    infoElem = main.querySelector('.info');
    errorElem.text = '';
    warningElem.text = '';

    // Get the input elements
    heightElem = main.querySelector('input[name="height"]');
    depthElem = main.querySelector('input[name="depth"]');
    lengthElem = main.querySelector('input[name="length"]');
    orderElem = main.querySelector('input[name="order"]');

    // The generate button and output elements
    generateElem = main.querySelector('button[name="generate"]');
    generateElem.onClick.listen((event) => compute());
    plotElem = main.querySelector('#plot');
    outputElem = main.querySelector('output');
    outputElem.innerHtml += "\n\nRaschiiDart version $version";

    checkInput();
  }

  /// Return wave height, depth and wave length
  List<double> waveParams() {
    double height, depth, length;
    errorElem.innerHtml = '';
    warningElem.innerHtml = '';
    inputOk = true;

    if (heightElem.checkValidity())
      height = double.parse(heightElem.value);
    else {
      inputOk = false;
      errorElem.innerHtml = 'Could not parse wave height, not a valid number!';
    }
    if (depthElem.checkValidity())
      depth = double.parse(depthElem.value);
    else {
      inputOk = false;
      errorElem.innerHtml = 'Could not parse water depth, not a valid number!';
    }
    if (lengthElem.checkValidity())
      length = double.parse(lengthElem.value);
    else {
      inputOk = false;
      errorElem.innerHtml = 'Could not parse wave length, not a valid number!';
    }
    return [height, depth, length];
  }

  /// Check that the wave input is reasonable (not breaking)
  void checkInput() {
    var wp = waveParams();
    if (!inputOk) return;

    if (!orderElem.checkValidity()) {
      inputOk = false;
      errorElem.innerHtml = 'Could not parse model order!';
    }

    double height = wp[0];
    double depth = wp[1];
    double length = wp[2];
    List<String> msg = check_breaking_criteria(height, depth, length);
    if (msg[0] != '') {
      errorElem.innerHtml = '<b>Results may be nonsensical!</b><br>' + newline2Ul(msg[0]);
    }
    warningElem.innerHtml = newline2Ul(msg[1]);
  }

  void compute() {
    plotElem.children.clear();
    outputElem.text = 'Computing ...';

    // Get input
    var wp = waveParams();
    checkInput();
    if (!inputOk) {
      outputElem.text += ' ERROR';
      return;
    }
    String modelName = modelElem.value;
    double height = wp[0];
    double depth = wp[1];
    double length = wp[2];
    int N = int.parse(orderElem.value);

    // Construct the wave model. May take some time
    wave = constructWaveModel(modelName, height, depth, length, N);

    // Report any problems
    if (wave.get_errors() != '')
      errorElem.innerHtml += '<b>Wave model reported errors:</b>' + newline2Ul(wave.get_errors());
    if (wave.get_warnings() != '')
      warningElem.innerHtml += '<b>Wave model warnings:</b>' + newline2Ul(wave.get_warnings());

    int Nx = 100;
    var x = new List<double>.generate(Nx, (int i) => i * length / (2 * (Nx - 1)));
    var eta = wave.eta(x);
    plot_wave(x, eta);

    outputElem.text = """Summary of results:
    Surface elevation maximum = ${eta.reduce(max).toStringAsFixed(3)}
    Surface elevation minimum = ${eta.reduce(min).toStringAsFixed(3)}
    Horizontal crest particle speed  = ${wave.velocity(x[0], eta[0])[0].toStringAsFixed(3 )}
    Horizontal trough particle speed = ${wave.velocity(x[Nx - 1], eta[Nx - 1])[0].toStringAsFixed(3 )}
    Wave number    = ${wave.k.toStringAsFixed(5)}
    Wave frequency = ${wave.omega.toStringAsFixed(5)}
    Wave period    = ${(2 * PI / wave.omega).toStringAsFixed(2)}
    Phase speed    = ${wave.c.toStringAsFixed(3 )}
    \n""" + wave.info();
    infoElem.innerHtml = '';
  }

  void plot_wave(List<double> x, List<double> eta) {
    var svg = new SvgSvgElement();
    svg.setAttribute('preserveAspectRatio', 'none');
    plotElem.children.add(svg);

    // Coordinates of the water domain
    List<double> xpos = [], ypos = [];
    xpos.add(0.0); ypos.add(0.0);
    xpos.addAll(x);
    ypos.addAll(eta);
    xpos.add(xpos[xpos.length - 1]);
    ypos.add(0.0);

    // Horizontal axis limits
    double xmin = x[0];
    double xmax = x[x.length - 1];

    // Vertical axis limits
    double eta_min = eta.reduce(min);
    double eta_max = eta.reduce(max);
    //double ymin = max(0.0, eta_min - (eta_max - eta_min) * 10);
    //ymin = max((eta_max + eta_min) / 2 - (xmax - xmin) * 2, ymin);
    double ymin = max(eta_min - (eta_max - eta_min) * 0.4, 0.0);
    double ymax = eta_max + (eta_max - eta_min) * 0.4;

    var plt = new Plotter(svg);
    plt.setView(xmin, xmax, ymin, ymax);
    plt.plotPolygon(xpos, ypos);
    plt.addOnClickDisplay(svg, showInfo);
  }

  void showInfo(double x, double y) {
    double e = wave.eta([x])[0];
    String info = 'You clicked on x = ${x.toStringAsFixed(4)}, z = ${y.toStringAsFixed(4)}';
    if (y > e) {
      info += ' (Air)';
    } else {
      info += ' (Water)';
      var vel = wave.velocity(x, y);
      info += '<br>Horizontal particle velocity: ${vel[0].toStringAsFixed(4)}';
      info += '<br>Vertical particle velocity:   ${vel[1].toStringAsFixed(4)}';
    }
    infoElem.innerHtml = info;
  }
}


/// Convert '1\ntwo\nthree\n' to '<ul><li>1</li><li>two</li><li>three</li></ul>
String newline2Ul(String inp) {
  String inp2 = inp.trim();
  if (inp2 == '') return '';
  return '<ul><li>' + inp2.replaceAll('\n', '</li><li>') + '</li></ul>';
}


main() {
  new RaschiiWeb(querySelector('#raschii'));
}