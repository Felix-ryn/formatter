from matrix import Matrix
from operations.adder import add_matrices
from operations.multiplier import multiply_matrices
from utilities import print_matrix

if __name__ == "__main__":
    matriks_a = Matrix([[1, 2], [3, 4]])
    matriks_b = Matrix([[5, 6], [7, 8]])

    print("Hasil Penjumlahan:")
    hasil_penjumlahan = add_matrices(matriks_a, matriks_b)
    print_matrix(hasil_penjumlahan)

    print("\nHasil Perkalian:")
    hasil_perkalian = multiply_matrices(matriks_a, matriks_b)
    print_matrix(hasil_perkalian)
