# operations/linear_regression.py

import numpy as np
from matrix import Matrix

def linear_regression(x_values, y_values):
    """
    Menghitung regresi linear sederhana (y = a + b*x)
    x_values dan y_values bisa berupa list atau numpy array
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
    b = b_num / b_den

    # hitung intercept (a)
    a = mean_y - b * mean_x

    return a, b


def predict(x_new, a, b):
    """Prediksi nilai y berdasarkan model regresi linear."""
    return a + b * np.array(x_new)
