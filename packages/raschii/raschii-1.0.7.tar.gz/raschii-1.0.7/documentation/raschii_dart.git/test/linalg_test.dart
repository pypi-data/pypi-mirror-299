import 'dart:math';
import "package:test/test.dart";
import '../support/linalg.dart';
import '../support/lu_decomposition.dart';
import 'utils.dart';

void main() {
  test("Basic vector operations", () {
    int N = 5;
    var vec = new Vector(N);
    for (var i = 0; i < N; i++) {
      expect(vec[i], equals(0.0));
      vec[i] = 1.0 * i;
    }
    expect(vec.data.reduce(min), equals(0.0));
    expect(vec.data.reduce(max), equals(N - 1.0));

    var vec2 = new Vector(N);
    vec2.assign(vec);
    expect(vec.toString(), equals(vec2.toString()));

    vec2.scale(2.0);
    expect(vec2[N - 1], equals((N - 1) * 2));

    vec2.axpy(-2.0, vec);
    expect(vec2.data.reduce(min), equals(0.0));
    expect(vec2.data.reduce(max), equals(0.0));

    var vec3 = new Vector.fromList([2.0, 4.0]);
    expect(vec3.size, equals(2));
    expect(vec3[0], equals(2.0));
    expect(vec3[1], equals(4.0));

    // Test alternative constructors
    var vec4 = new Vector.fromList([0.0, 1.0, 2.0, 3.0]);
    var vec5 = new Vector.arange(4);
    var vec6 = vec4.copy();
    for (var i = 0; i < 4; i++) {
      expect(vec4[i], equals(i.toDouble()));
      expect(vec5[i], equals(i.toDouble()));
      expect(vec6[i], equals(i.toDouble()));
    }
    expect(vec4.size, equals(4));
    expect(vec5.size, equals(4));
    expect(vec6.size, equals(4));
  });

  test("VectorView", () {
    var vec = new Vector.arange(10);
    var view1 = vec.view(0, 1);
    view1[0] = 5.0;
    var view2 = vec.view(5, 10);
    view2[0] = 9.0;
    view2[4] = 0.0;
    expect(view2[3], equals(8.0));

    var vec2 = new Vector.fromList([5.0, 1.0, 2.0, 3.0, 4.0, 9.0, 6.0,
                                    7.0, 8.0, 0.0]);
    for (var i = 0; i < vec.size; i++) {
      expect(vec[i], equals(vec2[i]));
    }
  });

  test("Basic matrix operations", () {
    var A = new Matrix(2, 2);
    var b = new Vector(2);
    A.set(0, 0, 1.0);
    A.set(0, 1, 2.0);
    A.set(1, 0, 3.0);
    A.set(1, 1, 4.0);
    b[0] = 1.0;
    b[1] = 2.0;
    var x = A.dot(b);
    expect(x[0], equals(1.0 * 1.0 + 2.0 * 2.0));
    expect(x[1], equals(3.0 * 1.0 + 4.0 * 2.0));

    expect(A[0][0], equals(1.0));
    A.add(0, 0, -1.0);
    expect(A[0][0], equals(0.0));

  });

  test("LU-decomposition", () {
    // Diagonal matrix solve and set / get operations
    int N = 5;
    var A = new Matrix(N, N);
    var b = new Vector(N);
    for (var i = 0; i < N; i++) {
      A.set(i, i, 2.0);
      b[i] = 84.0;
    }
    expect(A.data.data.reduce(min), equals(0.0));
    expect(A.data.data.reduce(max), equals(2.0));
    var x = new Vector(N);
    A.solve_lup(b, x);
    expect(x.data.reduce(min), near(42.0, 1e-14));
    expect(x.data.reduce(max), near(42.0, 1e-14));
    expect(A.get(1, 1), equals(2.0));

    // 2x2 full matrix solve
    A = new Matrix(2, 2);
    b = new Vector(2);
    A.set(0, 0, 7.0);
    A.set(0, 1, 5.0);
    A.set(1, 0, 3.0);
    A.set(1, 1, -2.0);
    b[0] = 3.0;
    b[1] = 22.0;
    x = new Vector(2);
    A.solve_lup(b, x);
    expect(x[0], near(4.0, 1e-14));
    expect(x[1], near(-5.0, 1e-14));

    // Inappropriately sized rhs vector
    b = new Vector(3); // to long vector
    expect(() => A.solve_lup(b), throwsA(new isInstanceOf<LinAlgException>()));

    // Singular test case from Apache Commons Math
    // 4th row = 1st + 2nd
    var singularMat = new Matrix.fromLists([
      [1.0, 2.0,   3.0,    4.0],
      [2.0, 5.0,   3.0,    4.0],
      [7.0, 3.0, 256.0, 1930.0],
      [3.0, 7.0,   6.0,    8.0]]);
    b = new Vector(4); // correct length, but matrix is singular
    expect(() => singularMat.solve_lup(b),
           throwsA(new isInstanceOf<SingularMatrixException>()));
    
    // Non-singular test case from Apache CommonsMath
    var testMat = new Matrix.fromLists([
      [1.0, 2.0, 3.0],
      [2.0, 5.0, 3.0],
      [1.0, 0.0, 8.0]]);
    x = testMat.solve_lup(new Vector.fromList([1.0, 2.0, 3.0]));
    expect(x[0], near(19.0, 1e-14));
    expect(x[1], near(-6.0, 1e-14));
    expect(x[2], near(-2.0, 1e-14));
    x = testMat.solve_lup(new Vector.fromList([0.0, -5.0, 1.0]));
    expect(x[0], near(-71.0, 1e-13));
    expect(x[1], near( 22.0, 1e-14));
    expect(x[2], near(  9.0, 1e-14));
  });

  test("trapz", () {
    expect(trapz(new Vector.arange(0)), equals(0.0));
    expect(trapz(new Vector.arange(1)), equals(0.0));
    expect(trapz(new Vector.arange(2)), near(0.5));
    expect(trapz(new Vector.arange(3)), near(2.0));
    expect(trapz(new Vector.arange(4)), near(4.5));
  });
}
