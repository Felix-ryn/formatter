from validators.is_square import is_square
def is_symmetric(matrix):
    """
    Memeriksa apakah sebuah matriks adalah simetris.
    """
    if not is_square(matrix):
        return False
    n = len(matrix)
    for i in range(n):
        for j in range(i, n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True
