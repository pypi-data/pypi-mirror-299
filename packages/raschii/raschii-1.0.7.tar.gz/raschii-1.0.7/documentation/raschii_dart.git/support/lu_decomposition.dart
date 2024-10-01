/// Decompose matrices into LUP-form (LU with partial pivoting)
///
/// This module implements LU decomposition and solution of linear
/// equations using LU decomposed matrices. The code is a direct port of
/// the Apache Commons Math code (org.apache.commons.math3.linear
/// LUDecomposition.java) extracted on June 1. 2018. The code (in the
/// Apache repo) was last changed on 2014-09-22 (commit abffaf334c). The
/// LICENCE of the code is the same as that of RaschiiDart, the Apache
/// 2.0 license.
/// 
/// Dart port by Tormod Landet, 2018
import 'linalg.dart';

/* This copyright notice is from the original Java sources:
 *
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

class LupException extends LinAlgException {
  LupException(String message) : super(message);
}

class NonSquareMatrixException extends LupException {
  NonSquareMatrixException() : super("The given matrix is not square!");
}

class SingularMatrixException extends LupException {
  SingularMatrixException() : super("The given matrix is singular!");
}

/// Decompose square matrices into LUP-form (LU with partial pivoting)
///
/// The LUP-decomposition of a matrix A consists of three matrices L, U
/// and P that satisfy: P×A = L×U. L is lower triangular (with unit
/// diagonal terms), U is upper triangular and P is a permutation matrix.
/// All matrices are m×m.
///
/// As shown by the presence of the P matrix, this decomposition is
/// implemented using partial pivoting.
///
/// This class is based on the class with similar name from the
/// [JAMA](http://math.nist.gov/javanumerics/jama/) library.
///
/// Added for Dart port: This code was ported from the Apache Commons
/// Math linear algebra library (written in Java) to Dart by Tormod
/// Landet in June 2018.
class LupDecomposition {
  /// Entries of LU decomposition.
  Matrix lu;

  /// Pivot permutation associated with LU decomposition.
  List<int> pivot;

  /// Parity of the permutation associated with the LU decomposition.
  bool even;

  /// Singularity indicator
  bool singular;

  /// Calculates the LU-decomposition of the given matrix.
  ///
  /// This constructor uses 1e-11 as default value for the singularity
  /// threshold. The [matrix] to decompose must be square and will not
  /// be changed. The [singularityThreshold] is used to determine if a
  /// matrix is singular (based on partial row norm). Throws
  /// [NonSquareMatrixException] if the matrix in not square.
  LupDecomposition(Matrix matrix, [double singularityThreshold = 1e-11]) {
    if (matrix.N != matrix.M) throw new NonSquareMatrixException();

    final int m = matrix.N;
    lu = new Matrix(m, m);
    lu.assign(matrix);
    pivot = new List<int>(m);

    // Initialize permutation array and parity
    for (int row = 0; row < m; row++) {
      pivot[row] = row;
    }
    even = true;
    singular = false;

    // Loop over columns
    for (int col = 0; col < m; col++) {
      // upper
      for (int row = 0; row < col; row++) {
        double sum = lu.get(row, col);
        for (int i = 0; i < row; i++) {
          sum -= lu.get(row, i) * lu.get(i, col);
        }
        lu.set(row, col, sum);
      }

      // lower
      int max = col; // permutation row
      double largest = double.NEGATIVE_INFINITY;
      for (int row = col; row < m; row++) {
        double sum = lu.get(row, col);
        for (int i = 0; i < col; i++) {
          sum -= lu.get(row, i) * lu.get(i, col);
        }
        lu.set(row, col, sum);

        // maintain best permutation choice
        if (sum.abs() > largest) {
          largest = sum.abs();
          max = row;
        }
      }

      // Singularity check
      if (lu.get(max, col).abs() < singularityThreshold) {
        singular = true;
        return;
      }

      // Pivot if necessary
      if (max != col) {
        double tmp = 0.0;
        for (int i = 0; i < m; i++) {
          tmp = lu.get(max, i);
          lu.set(max, i, lu.get(col, i));
          lu.set(col, i, tmp);
        }
        int temp = pivot[max];
        pivot[max] = pivot[col];
        pivot[col] = temp;
        even = !even;
      }

      // Divide the lower elements by the "winning" diagonal elt.
      final double luDiag = lu.get(col, col);
      for (int row = col + 1; row < m; row++) {
        lu.set(row, col, lu.get(row, col) / luDiag);
      }
    }
  }

  /// Solve A x = b given a right hand side [b] for this matrix
  ///
  /// Modifies the input vector [x] if it is given, otherwise
  /// creates a new vector. In any case [x] is returned.
  Vector solve(final Vector b, [Vector x]) {
    if (b.size != lu.N) throw new LinAlgException('${b.size} != ${lu.N}');
    if (x == null) x = new Vector(b.size);
    if (x.size != lu.N) throw new LinAlgException('${x.size} != ${lu.N}');
    if (singular) throw new SingularMatrixException();

    // Size of system
    final int m = pivot.length;

    // Apply permutations to b and store temporarily in x
    for (int row = 0; row < m; row++) {
      x[row] = b[pivot[row]];
    }

    // Solve LY = b
    for (int col = 0; col < m; col++) {
      final double bpCol = x[col];
      for (int i = col + 1; i < m; i++) {
        x[i] -= bpCol * lu.get(i, col);
      }
    }

    // Solve UX = Y
    for (int col = m - 1; col >= 0; col--) {
      x[col] /= lu.get(col, col);
      final double bpCol = x[col];
      for (int i = 0; i < col; i++) {
        x[i] -= bpCol * lu.get(i, col);
      }
    }
    return x;
  }
}
