# transpose.py
from matrix import Matrix

def transpose_matrix(matrix):
    """
    Mengembalikan transpose dari matriks.
    """
    transposed_data = [[matrix.data[j][i] for j in range(matrix.rows)] for i in range(matrix.cols)]
    return Matrix(transposed_data)
