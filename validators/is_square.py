def is_square(matrix):
    """
    Memeriksa apakah sebuah matriks (list of lists) adalah matr>    """
    if not matrix or not isinstance(matrix, list):
        return False
    rows = len(matrix)
    for row in matrix:
        if not isinstance(row, list) or len(row) != rows:
            return False
    return True
