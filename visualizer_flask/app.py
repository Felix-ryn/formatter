import os
import sys
import pandas as pd
import argparse
from flask import Flask, render_template

# --- Pastikan main.py bisa diimport dari folder induk ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from main import main as run_formatter  # Sekarang pasti bisa diimport

app = Flask(__name__)

# Argumen CLI untuk app Flask
def parse_args():
    parser = argparse.ArgumentParser(description="Run Flask visualizer + formatter")
    parser.add_argument("--a", required=True, help="Path ke CSV untuk matriks A")
    parser.add_argument("--b", help="Path ke CSV untuk matriks B (opsional)")
    parser.add_argument("--skip-header", action="store_true", help="Lewatkan baris header")
    return parser.parse_args()


def run_formatter_once(args):
    """
    Jalankan seluruh proses di main.py satu kali sebelum Flask aktif.
    """
    try:
        print(f"[INFO] Menjalankan formatter untuk: {args.a}")
        sys_argv_backup = sys.argv.copy()
        sys.argv = ["main.py", "--a", args.a]
        if args.b:
            sys.argv += ["--b", args.b]
        if args.skip_header:
            sys.argv += ["--skip-header"]
        run_formatter()  # Panggil langsung fungsi main()
        sys.argv = sys_argv_backup
    except Exception as e:
        print(f"[ERROR] Gagal menjalankan formatter: {e}")


# Lokasi default hasil ekspor CSV
CSV_FILE_PATH = os.path.join(BASE_DIR, "matriks_a_copy.csv")

def get_chart_data():
    """
    Memuat data CSV dan mengembalikan dict untuk Chart.js
    """
    try:
        df = pd.read_csv(CSV_FILE_PATH, header=None)
        labels = df[0].astype(str).tolist()
        values = df.iloc[:, -1].tolist()  # Kolom terakhir sebagai nilai
        chart_data = {
            "labels": labels,
            "data_values": values,
            "dataset_label": "Nilai Matriks (Kolom Terakhir)"
        }
        return chart_data
    except FileNotFoundError:
        print(f"[ERROR] File CSV tidak ditemukan di {CSV_FILE_PATH}")
        return {"labels": ["Error"], "data_values": [0], "dataset_label": "File Not Found"}
    except Exception as e:
        print(f"[ERROR] Kesalahan saat memproses data: {e}")
        return {"labels": ["Error"], "data_values": [0], "dataset_label": "Data Error"}


@app.route("/")
def index():
    data_dict = get_chart_data()
    return render_template("index.html", chart_data=data_dict)


if __name__ == "__main__":
    args = parse_args()
    run_formatter_once(args)
    print("[INFO] Menjalankan Flask server...")
    app.run(debug=True)
