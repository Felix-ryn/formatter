def print_matrix(matrix):
    """
    Mencetak isi dari objek matriks.
    """
    for row in matrix.data:
        print(row)

def find_determinant(matrix):
    """
    Menghitung determinan dari matriks 2x2 atau 3x3.
    """
    n = len(matrix)
    if not is_square(matrix):
        raise ValueError("Matrix must be a square matrix to find its determinant.")

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


def is_square(matrix):
    """
    Memeriksa apakah sebuah matriks adalah matriks persegi.
    """
    if not matrix or not isinstance(matrix, list):
        return False

    rows = len(matrix)
    for row in matrix:
        if not isinstance(row, list) or len(row) != rows:
            return False

    return True


def is_symmetric(matrix):
    """
    Memeriksa apakah sebuah matriks adalah matriks simetris.
    """
    if not is_square(matrix):
        return False

    n = len(matrix)
    for i in range(n):
        for j in range(i, n):
            if matrix[i][j] != matrix[j][i]:
                return False

    return True
