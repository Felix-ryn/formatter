# determinant.py
from ..utilities.validators import is_square

def find_determinant(matrix):
    """
    Menghitung determinan dari matriks persegi 2x2 atau 3x3.
    matrix: list of lists
    """
    if not is_square(matrix):
        raise ValueError("Matrix must be a square matrix to find its determinant.")
    n = len(matrix)
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    elif n == 3:
        det = (
            matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
            - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
            + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
        )
        return det
    else:
        raise NotImplementedError("Determinant calculation is only supported for 2x2 and 3x3 matrices.")
