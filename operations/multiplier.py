# multiplier.py
from matrix import Matrix
from validators.is_square import is_square  # opsional untuk validasi tambahan

def multiply_matrices(matrix1, matrix2):
    """
    Perkalian matriks (mengembalikan Matrix).
    Implementasi sederhana (O(n^3)).
    """
    if matrix1.cols != matrix2.rows:
        raise ValueError("Jumlah kolom matriks pertama harus sama dengan jumlah baris matriks kedua.")

    result_data = [
        [
            sum(matrix1.data[i][k] * matrix2.data[k][j] for k in range(matrix1.cols))
            for j in range(matrix2.cols)
        ]
        for i in range(matrix1.rows)
    ]
    return Matrix(result_data)
