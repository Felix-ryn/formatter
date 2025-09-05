def is_identity(matrix):
    """
    Memeriksa apakah sebuah matriks adalah matriks identitas.
    """
    # 1. Periksa apakah matriks adalah matriks persegi
    if len(matrix.data) != len(matrix.data[0]):
        return False

    # 2. Periksa elemen-elemen matriks
    for i in range(len(matrix.data)):
        for j in range(len(matrix.data[0])):
            # Periksa elemen diagonal (i == j)
            if i == j:
                if matrix.data[i][j] != 1:
                    return False
            # Periksa elemen non-diagonal (i != j)
            else:
                if matrix.data[i][j] != 0:
                    return False

    # 3. Jika semua elemen sesuai, matriks adalah identitas
    return True
