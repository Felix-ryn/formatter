import numpy as np

def multiple_linear_regression(X, y):
    # Konversi ke numpy
    X = np.array(X, dtype=float)
    y = np.array(y, dtype=float).reshape(-1, 1)

    # Hitung bobot dengan pseudo-inverse
    w = np.linalg.pinv(X) @ y
    return w
