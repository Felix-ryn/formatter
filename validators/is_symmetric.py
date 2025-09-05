def is_symmetric(matrix):
    """
    Memeriksa apakah sebuah matriks adalah simetris.
    """
    # 1. Periksa apakah matriks adalah matriks persegi
    if len(matrix.data) != len(matrix.data[0]):
        return False

    # 2. Periksa apakah elemen (i, j) sama dengan elemen (j, i)
    for i in range(len(matrix.data)):
        for j in range(len(matrix.data[0])):
            if matrix.data[i][j] != matrix.data[j][i]:
                return False

    # 3. Jika semua elemen sesuai, matriks adalah simetris
    return True
