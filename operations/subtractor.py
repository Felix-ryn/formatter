# subtractor.py
from matrix import Matrix
from validators.is_square import is_square  # opsional jika diperlukan

def subtract_matrices(matrix1, matrix2):
    """
    Pengurangan dua matriks.
    """
    if matrix1.rows != matrix2.rows or matrix1.cols != matrix2.cols:
        raise ValueError("Matriks harus memiliki dimensi yang sama untuk pengurangan.")

    result_data = [
        [matrix1.data[i][j] - matrix2.data[i][j] for j in range(matrix1.cols)]
        for i in range(matrix1.rows)
    ]
    return Matrix(result_data)
