import 'dart:svg' as svg;
import 'dart:html' as html;


class Plotter {
  svg.SvgSvgElement svgElement;
  double xmin, xmax, ymin, ymax;

  Plotter(svg.SvgSvgElement svgElement) {
    this.svgElement = svgElement;
  }

  svg.SvgElement plotPolygon(List<double> x, List<double> y) {
    var path = new svg.PathElement();
    String d = 'M';
    for (var i = 0; i < x.length; i++) {
      d += '${x[i]},${y[i]} ';
    }
    path.setAttribute('d', d + 'z');
    path.setAttribute('fill', '#687dc1');
    //path.setAttribute('fill-opacity', '0.6');

    // Safari does not support transforms directly on svg (yet)
    // TODO: remove this cludge in some month (written May 2018)
    //svgElement.children.add(path);
    var g = new svg.GElement();
    g.setAttribute('transform', 'scale(1,-1)');
    g.children.add(path);
    svgElement.children.add(g);
    return path;
  }

  void addOnClickDisplay(svg.SvgElement el, Function callback) {
    el.onClick.listen((html.MouseEvent event){
      var pos = getPhysicalCoordinates(event.client.x, event.client.y);
      callback(pos[0], pos[1]);
    });
  }

  void setView(double xmin, double xmax, double ymin, double ymax) {
    // Safari does not support transforms directly on svg (yet)
    // TODO: remove this cludge in some month (written May 2018)
    //svgElement.setAttribute('transform', 'scale(1,-1)');
    double tmp = ymin;
    ymin = -ymax;
    ymax = -tmp;
    
    svgElement.setAttribute('viewBox', '$xmin $ymin ${xmax - xmin} ${ymax - ymin}');
    this.xmin = xmin;
    this.xmax = xmax;
    this.ymin = ymin;
    this.ymax = ymax;
  }

  /// Given client coordinates, return the physical wave coordinates
  List<double> getPhysicalCoordinates(double x, double y) {
      // This code returns slightly inaccurate numbers for some reason :-/
      //var pt = svgElement.createSvgPoint();
      //pt.x = event.client.x;
      //pt.y = event.client.y;
      //var svgCoordPt = pt.matrixTransform(svgElement.getScreenCtm().inverse());
      // return [svgCoordPt.x, svgCoordPt.y];

      // Get the size of the svg image and compute the coordinate transform
      var cr = svgElement.getBoundingClientRect();
      double fx = (x - cr.left) / cr.width;
      double fy = 1 - (y - cr.top) / cr.height;
      double dx = xmax - xmin;
      double dy = ymax - ymin;

      // Safari does not support transforms directly on svg (yet)
      // TODO: remove this cludge in some month (written May 2018)
      //return [xmin + fx * dx, ymin + fy * dy];
      return [xmin + fx * dx, -(ymax - fy * dy)];
  }
}