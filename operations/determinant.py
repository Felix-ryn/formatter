# determinant.py
from validators.is_square import is_square
from matrix import Matrix

def find_determinant(matrix):
    """
    Menghitung determinan dari matriks persegi 2x2 atau 3x3.
    matrix: Matrix (objek)
    """
    data = matrix.data if hasattr(matrix, "data") else matrix
    if not is_square(matrix.data):
        raise ValueError("Matrix harus persegi untuk menghitung determinan.")

    data = matrix.data
    n = len(data)

    if n == 2:
        return data[0][0] * data[1][1] - data[0][1] * data[1][0]
    elif n == 3:
        det = (
            data[0][0] * (data[1][1] * data[2][2] - data[1][2] * data[2][1])
            - data[0][1] * (data[1][0] * data[2][2] - data[1][2] * data[2][0])
            + data[0][2] * (data[1][0] * data[2][1] - data[1][1] * data[2][0])
        )
        return det
    else:
        raise NotImplementedError("Determinant hanya didukung untuk 2x2 dan 3x3.")
