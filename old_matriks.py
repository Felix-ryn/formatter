# old_matriks.py
class Matrix:
    """
    Kelas untuk merepresentasikan objek matriks (versi lama).
    """
    def __init__(self, data):
        if not isinstance(data, list) or not all(isinstance(row, list) for row in data):
            raise TypeError("Data harus berupa list of lists.")
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0
        if not all(len(row) == self.cols for row in data):
            raise ValueError("Semua baris harus memiliki jumlah kolom yang sama.")

def add_matrices(matrix1, matrix2):
    if matrix1.rows != matrix2.rows or matrix1.cols != matrix2.cols:
        raise ValueError("Matriks harus memiliki dimensi yang sama untuk penjumlahan.")
    result_data = [[0 for _ in range(matrix1.cols)] for _ in range(matrix1.rows)]
    for i in range(matrix1.rows):
        for j in range(matrix1.cols):
            result_data[i][j] = matrix1.data[i][j] + matrix2.data[i][j]
    return Matrix(result_data)

def subtract_matrices(matrix1, matrix2):
    if matrix1.rows != matrix2.rows or matrix1.cols != matrix2.cols:
        raise ValueError("Matriks harus memiliki dimensi yang sama untuk pengurangan.")
    result_data = [[0 for _ in range(matrix1.cols)] for _ in range(matrix1.rows)]
    for i in range(matrix1.rows):
        for j in range(matrix1.cols):
            result_data[i][j] = matrix1.data[i][j] - matrix2.data[i][j]
    return Matrix(result_data)

def multiply_matrices(matrix1, matrix2):
    if matrix1.cols != matrix2.rows:
        raise ValueError("Jumlah kolom matriks pertama harus sama dengan jumlah baris matriks kedua untuk perkalian.")
    result_data = [[0 for _ in range(matrix2.cols)] for _ in range(matrix1.rows)]
    for i in range(matrix1.rows):
        for j in range(matrix2.cols):
            for k in range(matrix1.cols):
                result_data[i][j] += matrix1.data[i][k] * matrix2.data[k][j]
    return Matrix(result_data)

def print_matrix(matrix):
    for row in matrix.data:
        print(row)

if __name__ == "__main__":
    matriks_a = Matrix([[1, 2], [3, 4]])
    matriks_b = Matrix([[5, 6], [7, 8]])
    print("Hasil Penjumlahan:")
    hasil_penjumlahan = add_matrices(matriks_a, matriks_b)
    print_matrix(hasil_penjumlahan)
    print("\nHasil Perkalian:")
    hasil_perkalian = multiply_matrices(matriks_a, matriks_b)
    print_matrix(hasil_perkalian)
