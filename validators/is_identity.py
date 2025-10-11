def is_identity(matrix):
    """
    Memeriksa apakah sebuah matriks adalah matriks identitas.
    """
    if not matrix or not isinstance(matrix, list):
        return False
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if (i == j and matrix[i][j] != 1) or (i != j and matrix[i][j] != 0):
                return False
    return True
