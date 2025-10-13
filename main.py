# main.py

import os
import argparse
import sys
import time

#import kelas matrix
from matrix import Matrix

# === Import dari package internal ===
from utilities.csv_loader import load_matrix_from_csv
from utilities.formatter import print_matrix
from operations.adder import add_matrices
from operations.subtractor import subtract_matrices # Import Subtractor
from operations.multiplier import multiply_matrices
from exporters.csv_exporter import export_to_csv
from exporters.json_exporter import export_to_json
from operations.inverse import inverse_matrix
from operations.transpose import transpose_matrix
# Import kedua fungsi regresi
from operations.linear_regression import linear_regression, predict, multiple_linear_regression 

# === Import validator baru ===
from validators.is_square import is_square
from validators.is_symmetric import is_symmetric
from validators.is_identity import is_identity


def normalize_wsl_path(path: str) -> str:
    if not path:
        return path
    p = path.strip()
    if p.startswith("\\\\wsl.localhost\\") or p.startswith("\\\\wsl$\\"):
        parts = p.split("\\")
        if len(parts) >= 5:
            rest = parts[4:]
            return "/" + "/".join(rest)
        return p.replace("\\", "/")
    if os.name == "posix" and "\\" in p:
        return p.replace("\\", "/")
    return p


def parse_args():
    p = argparse.ArgumentParser(description="Load CSV(s) and run matrix operations.")
    p.add_argument("--a", required=True, help="Path ke CSV untuk matriks A (UNC WSL atau POSIX).")
    p.add_argument("--b", help="Path ke CSV untuk matriks B (opsional).")
    p.add_argument("--delimiter", help="CSV delimiter (default: comma). Jika tab gunakan '\\t'.", default=None)
    # Ubah action menjadi store_true, dan pengguna harus menambahkan flag --skip-header untuk house_multifeature.csv
    p.add_argument("--skip-header", action="store_true", help="Lewatkan baris header pada CSV.") 
    p.add_argument("--as-sparse", action="store_true", help="Paksa loader mengembalikan SparseMatrix.")
    p.add_argument("--sparse-threshold", type=float, default=0.5, help="Threshold proporsi nol untuk deteksi sparse.")
    p.add_argument("--impute", choices=["zero", "mean", "median", "drop"], default="zero",
                      help="Strategi imputasi untuk nilai kosong/non-numeric (default: zero).")
    p.add_argument("--normalize", choices=["minmax", "zscore"], default=None,
                      help="Normalisasi kolom numeric setelah imputasi.")
    p.add_argument("--no-export", action="store_true", help="Jangan export hasil ke file.")
    return p.parse_args()


def make_abs_and_normalize(path: str) -> str:
    if not path:
        return path
    normalized = normalize_wsl_path(path)
    if not os.path.isabs(normalized):
        normalized = os.path.abspath(normalized)
    return normalized


def main():
    args = parse_args()

    try:
        a_path = make_abs_and_normalize(args.a)
        b_path = make_abs_and_normalize(args.b) if args.b else None

        print(f"Loading A from: {a_path}")
        if b_path:
            print(f"Loading B from: {b_path}")

        # === Load matriks A ===
        matriks_a = load_matrix_from_csv(
            a_path,
            delimiter=args.delimiter,
            skip_header=args.skip_header,
            impute_strategy=args.impute,
            normalize=args.normalize,
            as_sparse=args.as_sparse,
            sparse_threshold=args.sparse_threshold
        )

        print("\n--- Matriks A (preview) ---")
        print(matriks_a)

        # === Validasi matriks ===
        print("\n[Validasi Matriks A]")
        try:
            print("Persegi?    :", is_square(matriks_a.data))
            print("Simetris?   :", is_symmetric(matriks_a.data))
            print("Identitas?  :", is_identity(matriks_a.data))
        except Exception as e:
            print(f"[WARNING] Validasi gagal (kemungkinan karena matriks besar): {e}")

        # === Jika matriks B juga disediakan ===
        if b_path:
            matriks_b = load_matrix_from_csv(
                b_path,
                delimiter=args.delimiter,
                skip_header=args.skip_header,
                impute_strategy=args.impute,
                normalize=args.normalize,
                as_sparse=args.as_sparse,
                sparse_threshold=args.sparse_threshold
            )
            print("\n--- Matriks B (preview) ---")
            print(matriks_b)

            # === Operasi dasar: Penjumlahan, Pengurangan, & Perkalian ===
            print("\n--- Menjalankan Operasi: Penjumlahan, Pengurangan, & Perkalian ---")
            
            # Addition
            try:
                hasil_penjumlahan = add_matrices(matriks_a, matriks_b)
                print("\nHasil Penjumlahan:")
                print_matrix(hasil_penjumlahan)
            except Exception as e:
                print(f"[ERROR] Gagal melakukan penjumlahan: {e}", file=sys.stderr)
                hasil_penjumlahan = None

            # Subtraction
            try:
                hasil_pengurangan = subtract_matrices(matriks_a, matriks_b)
                print("\nHasil Pengurangan:")
                print_matrix(hasil_pengurangan)
            except Exception as e:
                print(f"[ERROR] Gagal melakukan pengurangan: {e}", file=sys.stderr)
                hasil_pengurangan = None


            # Multiplication
            start_time = time.time()
            try:
                hasil_perkalian = multiply_matrices(matriks_a, matriks_b)
                print("\nHasil Perkalian:")
                print_matrix(hasil_perkalian)
                print(f"\n(Waktu perkalian: {time.time() - start_time:.4f} detik)")
            except Exception as e:
                print(f"[ERROR] Gagal melakukan perkalian: {e}", file=sys.stderr)
                hasil_perkalian = None

            # === Export hasil ===
            if not args.no_export and hasil_penjumlahan is not None:
                export_to_csv(hasil_penjumlahan, "hasil_penjumlahan.csv")
                export_to_json(hasil_penjumlahan, "hasil_penjumlahan.json")
                print("\nFile hasil disimpan: hasil_penjumlahan.csv, hasil_penjumlahan.json")


        # === Operasi tambahan: transpose, determinan, invers ===
        print("\n[Operasi Tambahan: Transpose, Determinan, Invers]")

        # Transpose
        try:
            transpose_a = transpose_matrix(matriks_a)
            print("\nTranspose Matriks A:")
            print_matrix(transpose_a)
        except Exception as e:
            print(f"[ERROR] Gagal menghitung transpose: {e}")
        
        # Determinan dan Invers (Hanya jika matriks kecil dan persegi)
        if matriks_a.rows <= 3 and matriks_a.cols == matriks_a.rows:
            try:
                from operations.determinant import find_determinant
                det_a = find_determinant(matriks_a)
                print(f"\nDeterminan Matriks A: {det_a}")
            except Exception as e:
                print(f"[ERROR] Gagal menghitung determinan: {e}")

            try:
                invers_a = inverse_matrix(matriks_a)
                print("\nInvers Matriks A:")
                print_matrix(invers_a)
            except Exception as e:
                print(f"[ERROR] Gagal menghitung invers: {e}")
        else:
             print("\n[INFO] Determinan/Inverse diskip: Matriks A bukan 2x2 atau 3x3 persegi.")


        # === Tambahan: Regresi Linear ===
        
        if matriks_a.rows < 2 or matriks_a.cols < 2:
             print("\n[ERROR] Matriks terlalu kecil untuk regresi.")
        else:
            # --- 1. Regresi Linear Sederhana (Simple LR) ---
            print("\n--- Simple Linear Regression (Luas vs. Harga) ---")
            try:
                # Kolom 0 = Luas (X); Kolom -1 = Harga (Y)
                x_values = [row[0] for row in matriks_a.data]
                y_values = [row[-1] for row in matriks_a.data]

                a, b = linear_regression(x_values, y_values)
                print(f"Persamaan regresi: y (Harga) = {a:.3f} + {b:.3f}x (Luas)")

                # contoh prediksi
                sample_x = [100, 150, 200]
                pred_y = predict(sample_x, a, b)
                print("\nContoh Prediksi:")
                for x, y in zip(sample_x, pred_y):
                    print(f"Luas = {x} => Harga_prediksi = {y:.3f}")
            except Exception as e:
                print(f"[ERROR] Gagal menghitung Simple Linear Regression: {e}")
                
            # --- 2. Multiple Linear Regression (MLR) ---
            print("\n--- Multiple Linear Regression (Luas, Kamar, Usia vs. Harga) ---")
            try:
                # Persiapan data: X_features = [Luas, Kamar, Usia], Y_target = [Harga]
                # Matriks A (4 kolom): [X1, X2, X3, Y]
                X_data = [row[:-1] for row in matriks_a.data] # Ambil semua kolom kecuali yang terakhir (Fitur)
                Y_data = [[row[-1]] for row in matriks_a.data] # Ambil kolom terakhir sebagai vektor kolom (Target)

                # Tambahkan kolom intercept (bias) '1' di depan X_data
                X_data_bias = [[1.0] + row for row in X_data]
                
                X_MLR = Matrix(X_data_bias)
                Y_MLR = Matrix(Y_data)
                
                print(f"Dimensi X_MLR (dengan bias): {X_MLR.rows}x{X_MLR.cols}")
                
                Beta = multiple_linear_regression(X_MLR, Y_MLR)
                
                if isinstance(Beta, str):
                    # Menangkap pesan error dari fungsi MLR (biasanya error invers)
                    print(f"\n[HASIL MLR TIDAK DAPAT DIHITUNG]: {Beta}") 
                else:
                    # Beta akan berbentuk Matriks 4x1: [b0, b1, b2, b3]
                    b0 = Beta.data[0][0] # Intercept
                    b1 = Beta.data[1][0] # Koefisien Luas
                    b2 = Beta.data[2][0] # Koefisien Kamar
                    b3 = Beta.data[3][0] # Koefisien Usia

                    print("\nHasil Multiple Linear Regression (Koefisien Beta):")
                    print(f"Intercept (b0): {b0:.3f}")
                    print(f"Luas (b1): {b1:.3f}")
                    print(f"Kamar (b2): {b2:.3f}")
                    print(f"Usia (b3): {b3:.3f}")
                    print(f"\nModel: Harga = {b0:.3f} + {b1:.3f}*Luas + {b2:.3f}*Kamar + {b3:.3f}*Usia")
                    
            except Exception as e:
                print(f"[ERROR] Gagal menghitung Multiple Linear Regression (Umum): {e}")
                print(f"[PETUNJUK] Periksa apakah operasi inverse_matrix Anda mendukung matriks {X_MLR.cols}x{X_MLR.cols}.")


        # === Export matriks jika tidak ada B ===
        if not b_path:
            print("\n(Hanya matriks A yang diberikan — tidak ada operasi B.)")
            if not args.no_export:
                export_to_csv(matriks_a, "matriks_a_copy.csv")
                export_to_json(matriks_a, "matriks_a_copy.json")
                print(" Matriks A diekspor ke: matriks_a_copy.csv, matriks_a_copy.json")

    except FileNotFoundError as fe:
        print(f"[ERROR] File tidak ditemukan: {fe}", file=sys.stderr)
        sys.exit(2)
    except ValueError as ve:
        print(f"[ERROR] Value error saat memproses file: {ve}", file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(f"[ERROR] Exception: {e}", file=sys.stderr)
        sys.exit(4)


if __name__ == "__main__":
    main()
