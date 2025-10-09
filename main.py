# main.py - jalankan sebagai: python3 -m matriks.main
from .matrix import Matrix
from .sparsematrix import SparseMatrix
from .operations.adder import add_matrices
from .operations.multiplier import multiply_matrices
from .utilities import print_matrix
from .exporters.json_exporter import export_to_json
from .exporters.csv_exporter import export_to_csv

import time

def create_sparse_data(size):
    data = [[0] * size for _ in range(size)]
    data[0][0] = 1
    data[size-1][size-1] = 1
    return data

def main():
    # --- Uji Coba Performa dengan SparseMatrix ---
    print("\n--- Menguji Solusi dengan SparseMatrix ---")
    sparse_data_100 = create_sparse_data(100)  # 100 instead of 1000 to avoid super long compute
    mat_a = SparseMatrix(sparse_data_100)
    mat_b = SparseMatrix(sparse_data_100)
    start_time = time.time()
    product_mat = multiply_matrices(mat_a, mat_b)
    end_time = time.time()
    print(f"Waktu yang dibutuhkan untuk perkalian: {end_time - start_time:.2f} detik")

    # --- Pembuktian OCP dengan Penjumlahan ---
    print("\n--- Pembuktian OCP dengan Penjumlahan ---")
    matriks_padat = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    matriks_jarang = SparseMatrix([[1, 0, 0], [0, 5, 0], [7, 0, 9]])
    hasil_penjumlahan = add_matrices(matriks_padat, matriks_jarang)
    print("Hasil Penjumlahan Matriks Biasa dan Sparse:")
    print(hasil_penjumlahan)

    # --- Uji Coba Operasi Normal ---
    print("\n--- Uji Coba Operasi Normal ---")
    matriks_a = Matrix([[1, 2], [3, 4]])
    matriks_b = Matrix([[5, 6], [7, 8]])

    print("Hasil Penjumlahan:")
    hasil_penjumlahan_normal = add_matrices(matriks_a, matriks_b)
    print_matrix(hasil_penjumlahan_normal)

    print("\nHasil Perkalian:")
    hasil_perkalian_normal = multiply_matrices(matriks_a, matriks_b)
    print_matrix(hasil_perkalian_normal)

    # --- Uji Coba Ekspor CSV ---
    print("\nMenyimpan Matriks C ke file CSV:")
    matrix_c = Matrix([[10, 20], [30, 40]])
    export_to_csv(matrix_c, "matriks_c.csv")

    # Ekspor ke JSON
    print("\nMengekspor matriks ke format JSON...")
    export_to_json(matrix_c, "matriks_output.json")

if __name__ == "__main__":
    main()
