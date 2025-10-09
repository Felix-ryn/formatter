# multiplier.py
from ..matrix import Matrix

def multiply_matrices(matrix1, matrix2):
    """
    Perkalian matriks (mengembalikan Matrix).
    Implementasi sederhana (O(n^3)).
    """
    if matrix1.cols != matrix2.rows:
        raise ValueError("Jumlah kolom matriks pertama harus sama dengan jumlah baris matriks kedua untuk perkalian.")
    result_data = [[0 for _ in range(matrix2.cols)] for _ in range(matrix1.rows)]
    for i in range(matrix1.rows):
        for j in range(matrix2.cols):
            s = 0
            for k in range(matrix1.cols):
                s += matrix1.data[i][k] * matrix2.data[k][j]
            result_data[i][j] = s
    return Matrix(result_data)
