# main.py

import os
import argparse
import sys
import time

# === Import dari package internal ===
from utilities.csv_loader import load_matrix_from_csv
from utilities.formatter import print_matrix
from operations.adder import add_matrices
from operations.multiplier import multiply_matrices
from exporters.csv_exporter import export_to_csv
from exporters.json_exporter import export_to_json

# === Import validator baru ===
from validators.is_square import is_square
from validators.is_symmetric import is_symmetric
from validators.is_identity import is_identity

def normalize_wsl_path(path: str) -> str:
    if not path:
        return path
    p = path.strip()
    # UNC: \\wsl.localhost\Distro\...
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

        # === Contoh penggunaan validator langsung ===
        print("\n[Validasi Matriks A]")
        try:
            print("Persegi?    :", is_square(matriks_a.data))
            print("Simetris?   :", is_symmetric(matriks_a.data))
            print("Identitas?  :", is_identity(matriks_a.data))
        except Exception as e:
            print(f"[WARNING] Validasi gagal: {e}")

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

            # === Operasi dasar ===
            print("\n--- Menjalankan Operasi: Penjumlahan & Perkalian ---")
            try:
                hasil_penjumlahan = add_matrices(matriks_a, matriks_b)
            except Exception as e:
                print(f"[ERROR] Gagal melakukan penjumlahan: {e}", file=sys.stderr)
                hasil_penjumlahan = None

            if hasil_penjumlahan is not None:
                print("\nHasil Penjumlahan:")
                print_matrix(hasil_penjumlahan)

            start_time = time.time()
            try:
                hasil_perkalian = multiply_matrices(matriks_a, matriks_b)
            except Exception as e:
                print(f"[ERROR] Gagal melakukan perkalian: {e}", file=sys.stderr)
                hasil_perkalian = None
            end_time = time.time()

            if hasil_perkalian is not None:
                print("\nHasil Perkalian:")
                print_matrix(hasil_perkalian)
                print(f"\n(Waktu perkalian: {end_time - start_time:.4f} detik)")

            # === Export hasil ===
            if not args.no_export and hasil_penjumlahan is not None:
                export_to_csv(hasil_penjumlahan, "hasil_penjumlahan.csv")
                export_to_json(hasil_penjumlahan, "hasil_penjumlahan.json")
                print("\nFile hasil disimpan: hasil_penjumlahan.csv, hasil_penjumlahan.json")

        else:
            print("\n(Hanya matriks A yang diberikan — tidak ada operasi B.)")
            if not args.no_export:
                export_to_csv(matriks_a, "matriks_a_copy.csv")
                export_to_json(matriks_a, "matriks_a_copy.json")
                print("Matriks A diekspor ke: matriks_a_copy.csv, matriks_a_copy.json")

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
