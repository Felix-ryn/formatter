# main.py
# Program utama untuk memuat matriks dari file CSV, melakukan operasi matriks,
# validasi sifat matriks, dan menjalankan regresi linear sederhana & multiple.

import os
import argparse
import sys
import time
from typing import Any

# Import class Matrix untuk merepresentasikan matriks
from matrix import Matrix

# === Import utility untuk input & output data ===
from utilities.csv_loader import load_matrix_from_csv       # Load CSV menjadi Matrix / SparseMatrix
from utilities.formatter import print_matrix                # Format tampilan matriks ke console

# === Import operasi dasar matriks ===
from operations.adder import add_matrices                   # Penjumlahan matriks
from operations.subtractor import subtract_matrices         # Pengurangan matriks
from operations.multiplier import multiply_matrices         # Perkalian matriks
from operations.inverse import inverse_matrix               # Invers matriks (dipakai hanya untuk matriks kecil)
from operations.transpose import transpose_matrix           # Transpose matriks

# === Import Regresi / MLR (gunakan mlr.py yang memakai pseudo-inverse) ===
from operations.linear_regression import linear_regression, predict
import operations.mlr as mlr_module  # multiple_linear_regression ada di sini (pakai pinv)

# === Import validator matriks ===
from validators.is_square import is_square
from validators.is_symmetric import is_symmetric
from validators.is_identity import is_identity

# fungsi eksporter
from exporters.csv_exporter import export_to_csv
from exporters.json_exporter import export_to_json


def normalize_wsl_path(path: str) -> str:
    """
    Menormalkan path ketika mengambil file dari Windows Subsystem for Linux (WSL).
    Mengubah path UNC Windows menjadi path POSIX jika perlu.
    """
    if not path:
        return path
    p = path.strip()

    # Path UNC WSL -> ubah menjadi format Linux
    if p.startswith("\\\\wsl.localhost\\") or p.startswith("\\\\wsl$\\"):
        parts = p.split("\\")
        if len(parts) >= 5:
            rest = parts[4:]
            return "/" + "/".join(rest)
        return p.replace("\\", "/")

    # Jika dijalankan di Linux tapi path mengandung backslash → ubah ke slash
    if os.name == "posix" and "\\" in p:
        return p.replace("\\", "/")

    return p


def parse_args():
    """
    Mengambil parameter dari command-line seperti:
    - lokasi file input matriks,
    - opsi sparse,
    - strategi imputasi,
    - opsi normalisasi.
    """
    p = argparse.ArgumentParser(description="Load CSV(s) and run matrix operations.")
    p.add_argument("--a", required=True, help="Path ke CSV untuk matriks A.")
    p.add_argument("--b", help="Path ke CSV untuk matriks B (opsional).")
    p.add_argument("--delimiter", default=None, help="Delimiter CSV (default koma).")
    p.add_argument("--skip-header", action="store_true", help="Lewatkan baris header CSV.")
    p.add_argument("--as-sparse", action="store_true", help="Paksa matriks dimuat sebagai SparseMatrix.")
    p.add_argument("--sparse-threshold", type=float, default=0.5,
                   help="Jika proporsi nol > threshold, pakai SparseMatrix otomatis.")
    p.add_argument("--impute", choices=["zero", "mean", "median", "drop"], default="zero",
                   help="Strategi isi nilai hilang.")
    p.add_argument("--normalize", choices=["minmax", "zscore"], default=None,
                   help="Normalisasi kolom numerik.")
    p.add_argument("--no-export", action="store_true", help="Matikan ekspor hasil ke file.")
    return p.parse_args()


def make_abs_and_normalize(path: str) -> str:
    """
    Normalisasi path + pastikan path berupa absolute path.
    """
    if not path:
        return path
    normalized = normalize_wsl_path(path)
    if not os.path.isabs(normalized):
        normalized = os.path.abspath(normalized)
    return normalized


def _print_matrix_or_obj(name: str, obj: Any):
    """
    Helper: jika obj punya attribute .data (Matrix-like) gunakan print_matrix,
    kalau bukan, print biasa.
    """
    print(f"\n{name}")
    if hasattr(obj, "data"):
        print_matrix(obj)
    else:
        print(obj)


def main():
    # Ambil semua argumen
    args = parse_args()

    try:
        # Normalisasi path file input
        a_path = make_abs_and_normalize(args.a)
        b_path = make_abs_and_normalize(args.b) if args.b else None

        print(f"Loading A from: {a_path}")
        if b_path:
            print(f"Loading B from: {b_path}")

        # === Load matriks A dengan opsi imputasi, normalisasi, dan deteksi sparse ===
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
        print_matrix(matriks_a)

        # === Validasi sifat matriks A ===
        print("\n[Validasi Matriks A]")
        print("Persegi?    :", is_square(matriks_a.data))
        print("Simetris?   :", is_symmetric(matriks_a.data))
        print("Identitas?  :", is_identity(matriks_a.data))

        # === Jika ada Matriks B ===
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
            print_matrix(matriks_b)

            print("\n--- Operasi Matriks (A & B) ---")

            # Penjumlahan
            try:
                hasil_penjumlahan = add_matrices(matriks_a, matriks_b)
                print("\nHasil Penjumlahan:")
                print_matrix(hasil_penjumlahan)
            except Exception as e:
                print(f"[ERROR] Penjumlahan gagal: {e}")
                hasil_penjumlahan = None

            # Pengurangan
            try:
                hasil_pengurangan = subtract_matrices(matriks_a, matriks_b)
                print("\nHasil Pengurangan:")
                print_matrix(hasil_pengurangan)
            except Exception as e:
                print(f"[ERROR] Pengurangan gagal: {e}")
                hasil_pengurangan = None

            # Perkalian
            try:
                start = time.time()
                hasil_perkalian = multiply_matrices(matriks_a, matriks_b)
                print("\nHasil Perkalian:")
                print_matrix(hasil_perkalian)
                print(f"\nWaktu eksekusi perkalian: {time.time() - start:.4f} detik")
            except Exception as e:
                print(f"[ERROR] Perkalian gagal: {e}")

            # Export hasil (jika tidak dinonaktifkan)
            if not args.no_export and hasil_penjumlahan is not None:
                export_to_csv(hasil_penjumlahan, "hasil_penjumlahan.csv")
                try:
                    export_to_json(hasil_penjumlahan, "hasil_penjumlahan.json")
                except Exception:
                    # jika json exporter belum ada / berbeda format, jangan crash
                    pass
                print("\nHasil diexport ke: hasil_penjumlahan.csv & hasil_penjumlahan.json")

        # === Operasi tambahan pada Matriks A ===
        print("\n[Operasi Tambahan]")

        # Transpose
        try:
            transpose_a = transpose_matrix(matriks_a)
            print("\nTranspose Matriks A:")
            print_matrix(transpose_a)
        except Exception as e:
            print(f"[ERROR] Transpose gagal: {e}")

        # Determinan & Invers hanya untuk matriks kecil (2x2 atau 3x3)
        if matriks_a.rows <= 3 and matriks_a.rows == matriks_a.cols:
            from operations.determinant import find_determinant
            try:
                print(f"\nDeterminan Matriks A: {find_determinant(matriks_a)}")
            except Exception:
                print("[ERROR] Gagal menghitung determinan")

            try:
                print("\nInvers Matriks A:")
                print_matrix(inverse_matrix(matriks_a))
            except Exception:
                print("[ERROR] Gagal menghitung invers")
        else:
            print("\n[INFO] Determinan dan invers dilewati: Matriks tidak persegi kecil.")

        # === Regresi Linear Sederhana ===
        if matriks_a.rows >= 2 and matriks_a.cols >= 2:
            print("\n--- Regresi Linear Sederhana (kolom 0 vs kolom terakhir) ---")

            # Ambil kolom X & Y
            x_values = [row[0] for row in matriks_a.data]
            y_values = [row[-1] for row in matriks_a.data]

            # Hitung model
            a, b = linear_regression(x_values, y_values)
            print(f"Model: y = {a:.3f} + {b:.3f}x")

            print("\nContoh prediksi:")
            for x, y_pred in zip([100, 150, 200], predict([100, 150, 200], a, b)):
                print(f"x={x} → y_pred={y_pred:.3f}")

            # === Multiple Linear Regression (pakai operations.mlr) ===
            print("\n--- Multiple Linear Regression ---")
            # X: tambah kolom bias (1.0), fitur = semua kolom kecuali target terakhir
            X = [[1.0] + row[:-1] for row in matriks_a.data]
            # Y: list target
            Y = [row[-1] for row in matriks_a.data]

            # Panggil MLR dari module mlr (kembalian list atau string error)
            try:
                Beta = mlr_module.multiple_linear_regression(X, Y)
            except Exception as e:
                Beta = f"Error: {e}"

            # Tampilkan hasil MLR:
            if isinstance(Beta, str):
                print(f"[ERROR] Tidak dapat menghitung MLR: {Beta}")
            else:
                # Beta bisa berupa list/array (koef per kolom)
                try:
                    # Pastikan iterable
                    print("\nKoefisien MLR (Beta):")
                    for i, coef in enumerate(Beta):
                        print(f"b{i} = {float(coef):.6f}")
                except Exception:
                    # Fallback: print mentah
                    print("Beta:", Beta)

        # Jika hanya matriks A yang diberikan, export langsung
        if not b_path and not args.no_export:
            try:
                export_to_csv(matriks_a, "matriks_a_copy.csv")
            except Exception as e:
                print(f"[WARN] Gagal export CSV: {e}")
            try:
                export_to_json(matriks_a, "matriks_a_copy.json")
            except Exception:
                # abaikan jika exporter json tidak kompatibel
                pass

            print("\nMatriks A diekspor ke: matriks_a_copy.csv & matriks_a_copy.json")

    except Exception as e:
        print(f"[ERROR] Program berhenti: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
