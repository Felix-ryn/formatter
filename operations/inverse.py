# inverse.py
from matrix import Matrix
from operations.determinant import find_determinant
from validators.is_square import is_square

def inverse_matrix(matrix):
    """
    Menghitung invers matriks 2x2 atau 3x3.
    """
    data = matrix.data
    if not is_square(data):
        raise ValueError("Matrix harus persegi untuk menghitung invers.")

    n = len(data)
    det = find_determinant(data)
    if det == 0:
        raise ValueError("Matriks singular, tidak memiliki invers.")

    # Kasus 2x2
    if n == 2:
        a, b = data[0]
        c, d = data[1]
        inv_data = [[d/det, -b/det], [-c/det, a/det]]
        return Matrix(inv_data)

    # Kasus 3x3 (pakai kofaktor)
    elif n == 3:
        cofactor = [[0]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                minor = [
                    [data[x][y] for y in range(3) if y != j]
                    for x in range(3) if x != i
                ]
                sign = (-1) ** (i + j)
                cofactor[i][j] = sign * find_determinant(minor)
        # transpose kofaktor
        cofactor_T = [[cofactor[j][i] for j in range(3)] for i in range(3)]
        inv_data = [[cofactor_T[i][j] / det for j in range(3)] for i in range(3)]
        return Matrix(inv_data)

    else:
        raise NotImplementedError("Inverse hanya didukung untuk matriks 2x2 dan 3x3.")
