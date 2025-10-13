# operations/linear_regression.py

import numpy as np
from matrix import Matrix
# Import operasi matriks yang sudah Anda buat
from .transpose import transpose_matrix
from .multiplier import multiply_matrices
from .inverse import inverse_matrix

def linear_regression(x_values, y_values):
    """
    Menghitung regresi linear sederhana (y = a + b*x).
    """
    if len(x_values) != len(y_values):
        raise ValueError("Panjang x dan y harus sama")

    x = np.array(x_values, dtype=float)
    y = np.array(y_values, dtype=float)

    n = len(x)
    mean_x = np.mean(x)
    mean_y = np.mean(y)

    # hitung slope (b)
    b_num = np.sum((x - mean_x) * (y - mean_y))
    b_den = np.sum((x - mean_x) ** 2)
    
    if b_den == 0:
        b = 0
    else:
        b = b_num / b_den

    # hitung intercept (a)
    a = mean_y - b * mean_x

    return a, b


def predict(x_new, a, b):
    """Prediksi nilai y berdasarkan model regresi linear sederhana."""
    return a + b * np.array(x_new)


def multiple_linear_regression(X_matrix: Matrix, Y_vector: Matrix):
    """
    Menghitung koefisien Multiple Linear Regression menggunakan Persamaan Normal:
    Beta = (X^T * X)^-1 * X^T * Y
    
    X_matrix: Matriks fitur [n x k] (sudah termasuk kolom 1s untuk intercept)
    Y_vector: Matriks target [n x 1]
    """
    if X_matrix.rows != Y_vector.rows or Y_vector.cols != 1:
        raise ValueError("Dimensi matriks X dan Y salah untuk MLR.")
        
    # 1. X Transpose (X^T)
    X_T = transpose_matrix(X_matrix)

    # 2. X^T * X
    XT_X = multiply_matrices(X_T, X_matrix)

    # 3. (X^T * X)^-1
    # Implementasi ini akan gagal jika matriks > 3x3 karena keterbatasan inverse_matrix.
    try:
        XT_X_inv = inverse_matrix(XT_X)
    except NotImplementedError:
        return "Error: Inverse (X^T X)^-1 gagal. Hanya 2x2 dan 3x3 yang didukung pada inverse_matrix."
    except ValueError as e:
        return f"Error: {e}"

    # 4. X^T * Y
    XT_Y = multiply_matrices(X_T, Y_vector)

    # 5. Beta = (X^T * X)^-1 * X^T * Y
    Beta = multiply_matrices(XT_X_inv, XT_Y)
    
    return Beta
