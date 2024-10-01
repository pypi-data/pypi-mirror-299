import 'dart:math';
import 'lu_decomposition.dart';

class LinAlgException implements Exception {
  String message;
  LinAlgException(this.message);
  String toString() => message;
}

class ConvergenceException extends LinAlgException {
  ConvergenceException(String method) : super('$method did not converge!');
}

// -- Vector classes -----------------------------------------------------

abstract class BaseVector {
  int get size;
  double operator [](int i);
  void operator []=(int i, double v);
}

/// A vector of doubles, length N
class Vector implements BaseVector {
  List<double> data;

  Vector(int N) {
    data = new List<double>(N);
    data.fillRange(0, N, 0.0);
  }

  Vector.fromList(List<double> list) {
    data = new List<double>(list.length);
    data.setAll(0, list);
  }

  Vector.arange(int N) {
    data = new List<double>(N);
    for (var i = 0; i < N; i++) {
      data[i] = i.toDouble();
    }
  }

  Vector.linspace(double start, double end, int N) {
    data = new List<double>(N);
    double dx = (end - start) / (N - 1);
    for (var i = 0; i < size; i++) {
      data[i] = start + i * dx;
    }
  }

  Vector copy() {
    var b = new Vector(size);
    b.assign(this);
    return b;
  }

  /// A read/write view of the vector starting from start (inclusive)
  /// to the end (not inclusive)
  VectorView view(int start, int end) => new VectorView(this, start, end);

  int get size => data.length;
  double operator [](int i) => data[i];
  void operator []=(int i, double v) => data[i] = v;

  void axpy(double scale, final Vector b) {
    if (b.size != size) throw new LinAlgException('${b.size} != $size');
    for (var i = 0; i < size; i++) {
      data[i] += scale * b.data[i];
    }
  }

  void assign(final Vector b) {
    if (b.size != size) throw new LinAlgException('${b.size} != $size');
    for (var i = 0; i < size; i++) {
      data[i] = b.data[i];
    }
  }

  /// Return the largest absolute value
  double abs_max() {
    double res = double.NEGATIVE_INFINITY;
    for (var i = 0; i < size; i++) {
      res = max(data[i].abs(), res);
    }
    return res;
  }

  void scale(double scale) {
    for (var i = 0; i < size; i++) {
      data[i] *= scale;
    }
  }

  List<double> toList() {
    return data.toList();
  }

  String toString() {
    return 'Vector(${data.toString()})';
  }
}

/// A view of part of a vector
class VectorView implements BaseVector {
  Vector vec;
  int offset;
  int size;

  /// A view of [vec] starting from [start] and going up to, but not
  /// including [end]. The view is writable and updates the underlying
  /// vector [vec].
  VectorView(this.vec, int start, int end)
      : offset = start,
        size = end - start;

  double operator [](int i) {
    if (i < 0) throw new LinAlgException('$i < 0');
    if (i >= size) throw new LinAlgException('$i >= $size');
    return vec.data[i + offset];
  }

  void operator []=(int i, double v) {
    if (i < 0) throw new LinAlgException('$i < 0');
    if (i >= size) throw new LinAlgException('$i >= $size');
    vec.data[i + offset] = v;
  }

  List<double> toList() {
    var list = new List<double>(size);
    for (var i = 0; i < size; i++) {
      list[i] = this[i];
    }
    return list;
  }

  String toString() {
    return 'VectorView(${toList().toString()})';
  }
}

// -- Matrix classes -----------------------------------------------------

/// A matrix of doubles, size N * M
class Matrix {
  Vector data;
  int N, M;

  Matrix(int N, int M) {
    this.N = N;
    this.M = M;
    data = new Vector(N * M);
  }

  Matrix.fromLists(List<List<double>> lists) {
    N = lists.length;
    if (N == 0) {
      M = 0;
    } else {
      M = lists[0].length;
    }
    data = new Vector(N * M);

    for (int i = 0; i < N; i++) {
      final int L = lists[i].length;
      if (L != M) throw new LinAlgException('$L != $M');
      for (int j = 0; j < M; j++) {
        set(i, j, lists[i][j]);
      }
    }
  }

  void assign(final Matrix b) {
    if (N != b.N || M != b.M) {
      throw new LinAlgException('Matrix sizes ($M, $N) and (${b.N}, ${b.M})'
          ' do not match!');
    }
    data.assign(b.data);
  }

  double get(int i, int j) {
    if (i < 0) throw new LinAlgException('$i < 0');
    if (i >= N) throw new LinAlgException('$i >= $N');
    if (j < 0) throw new LinAlgException('$j < 0');
    if (j >= M) throw new LinAlgException('$j >= $M');
    return data[i * M + j];
  }

  void set(int i, int j, double value) {
    if (i < 0) throw new LinAlgException('$i < 0');
    if (i >= N) throw new LinAlgException('$i >= $N');
    if (j < 0) throw new LinAlgException('$j < 0');
    if (j >= M) throw new LinAlgException('$j >= $M');
    data[i * M + j] = value;
  }

  void add(int i, int j, double value) {
    if (i < 0) throw new LinAlgException('$i < 0');
    if (i >= N) throw new LinAlgException('$i >= $N');
    if (j < 0) throw new LinAlgException('$j < 0');
    if (j >= M) throw new LinAlgException('$j >= $M');
    data[i * M + j] += value;
  }

  /// Get a writable view of a given row [i]
  VectorView operator [](int i) {
    if (i < 0) throw new LinAlgException('$i < 0');
    if (i >= N) throw new LinAlgException('$i >= $N');
    return new VectorView(data, i * M, (i + 1) * M);
  }

  Vector dot(final Vector vec) {
    var res = new Vector(N);
    for (var i = 0; i < N; i++) {
      for (var j = 0; j < M; j++) {
        res[i] += data[i * M + j] * vec[j];
      }
    }
    return res;
  }

  /// Solve A x = b for x using Lu factorization with partial pivoting
  Vector solve_lup(final Vector b, [Vector x]) {
    var lup_decomp = new LupDecomposition(this);
    return lup_decomp.solve(b, x);
  }

  String toString() {
    String s = 'Matrix([';
    for (var i = 0; i < N; i++) {
      if (i == 0)
        s += '[';
      else
        s += '        [';
      for (var j = 0; j < M; j++) {
        s += '${data[i * M + j].toStringAsExponential(5)}';
        if (j != M - 1) s += ', ';
      }
      if (i < N - 1)
        s += '],\n';
      else
        s += ']])';
    }
    return s;
  }
}

// -- Free functions -----------------------------------------------------

/// Trapezoidal rule with uniform dx = 1
double trapz(BaseVector vec) {
  final int N = vec.size;
  if (N < 2) return 0.0;
  double res = (vec[0] + vec[N - 1]) / 2;
  for (var i = 1; i < N - 1; i++) {
    res += vec[i];
  }
  return res;
}
