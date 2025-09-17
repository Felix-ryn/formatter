from matrix import Matrix
from operations.adder import add_matrices
from operations.multiplier import multiply_matrices
from utilities import print_matrix
from exporters.csv_exporter import export_to_csv

if __name__ == "__main__":
    # ... (kode demonstrasi lainnya)
    matrix_c = Matrix([[10, 20], [30, 40]])
    print("\nMenyimpan Matriks C ke file CSV:")
    export_to_csv(matrix_c, "matriks_c.csv")

if __name__ == "__main__":
    matriks_a = Matrix([[1, 2], [3, 4]])
    matriks_b = Matrix([[5, 6], [7, 8]])

    print("Hasil Penjumlahan:")
    hasil_penjumlahan = add_matrices(matriks_a, matriks_b)
    print_matrix(hasil_penjumlahan)

    print("\nHasil Perkalian:")
    hasil_perkalian = multiply_matrices(matriks_a, matriks_b)
    print_matrix(hasil_perkalian)
